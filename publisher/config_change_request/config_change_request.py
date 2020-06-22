"""This module is responsible for creating and publishing Protocol Buffer Objects via Pub/Sub
messages according to the configuration change request type specified in the template
submitted by the reporter of the Buganizer issue. It holds the Context, ConfigurationTypes,
EnqueueRule, RoutingRule, and QueueInfo classes and uses the strategy design pattern.
"""
from google.cloud import pubsub_v1
import constants
from config_change_request import config_change_pb2
import time

class Context:
  """Accepts a strategy in order to parse and publish a template.
  """
  def __init__(self, strategy):
    self._strategy = strategy

  def prepare_for_publish(self, template):
    """Use the selected strategy to attempt to parse the template.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      bool: True if the comment was in valid template format. False if not.
    """
    return self._strategy.parse_template(template)

  def pub(self):
    """Publish using whatever strategy is selected.
    """
    self._strategy.publish()

class ConfigurationTypes():
  """The parent class of the types of configurations(EnqueueRule, RoutingRule, QueueInfo)"""

  def __init__(self, reporter, config_change_type):
    self.config_change_type = config_change_type
    self.config_change_request = config_change_pb2.ConfigChangeRequest()
    self.config_change_request.reporter = reporter
    
  def get_callback(self, api_future, data, ref):
    """Wrap message data in the context of the callback function."""
    def callback(api_future):
        try:
            print("Published message with type {}. Message ID: {}".format(self.config_change_type, api_future.result()))
            ref["num_messages"] += 1
        except Exception:
            print("A problem occured when publishing {}: {}\n".format(data, api_future.exception()))
            raise
    return callback

  def publish(self):
    """Publish a message to a Pub/Sub topic.
    """
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(constants.PROJECT_ID, constants.TOPIC_NAME)
    ref = dict({"num_messages": 0})
    data = self.config_change_request.SerializeToString()
    api_future = client.publish(topic_path, data=data)
    api_future.add_done_callback(self.get_callback(api_future, data, ref))

class EnqueueRule(ConfigurationTypes):
  """Defines how EnqueueRule templates should be parsed"""

  def parse_template(self, template):
    """Parses the template into a Protocol Buffer object that will
     be ready to send, given it is valid.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      bool: True if the comment was in valid template format.
      False if not in valid template format.
    """
    #These keep track of the current line number of each specifier for EnqueueRule.
    #Starts at 1 since the first line is reserved for the Configuration specifier. 
    method_specifier_line_number = 1
    queue_specifier_line_number = 2
    features_specifier_line_number = 3
    priority_specifier_line_number = 4
    
    #Length of each specifier
    method_specifier_length = len(constants.ENQUEUE_RULE_METHOD_SPECIFIER)
    queue_specifier_length = len(constants.ENQUEUE_RULE_QUEUE_SPECIFIER)
    features_specifier_length = len(constants.ENQUEUE_RULE_FEATURES_SPECIFIER)
    priority_specifier_length = len(constants.ENQUEUE_RULE_PRIORITY_SPECIFIER)
    
    if (len(template) - 1) % constants.ENQUEUE_RULE_COMMAND_LINES_COUNT > 0:
        return False

    while priority_specifier_line_number <= len(template):
      change = self.config_change_request.enqueue_rule.Change()
      try:
        method_specifier = template[method_specifier_line_number][:method_specifier_length]
        queue_specifier = template[queue_specifier_line_number][:queue_specifier_length]
        features_specifier = template[features_specifier_line_number][:features_specifier_length]
        priority_specifier = template[priority_specifier_line_number][:priority_specifier_length]

        if method_specifier != constants.ENQUEUE_RULE_METHOD_SPECIFIER or queue_specifier != constants.ENQUEUE_RULE_QUEUE_SPECIFIER or \
        features_specifier != constants.ENQUEUE_RULE_FEATURES_SPECIFIER or priority_specifier != constants.ENQUEUE_RULE_PRIORITY_SPECIFIER:
          return False
      except Exception:
        return False

      change.method = template[method_specifier_line_number][method_specifier_length:]
      change.queue = template[queue_specifier_line_number][queue_specifier_length:]
      change.features.extend(template[features_specifier_line_number][features_specifier_length:].split(", "))
      change.priority = int(template[priority_specifier_line_number][priority_specifier_length:])
      self.config_change_request.enqueue_rule.changes.append(change)
      
      method_specifier_line_number += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
      queue_specifier_line_number += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
      features_specifier_line_number += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
      priority_specifier_line_number += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
      
    return True

class RoutingRule(ConfigurationTypes):
  """Defines how RoutingRule templates should be parsed"""

  def parse_template(self, template):
    """Parses the template into a Protocol Buffer object that will be ready to send,
    given it is valid.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      bool: True if the comment was in valid template format.
      False if not in valid template format.
    """
    #These keep track of the current line number of each specifier for RoutingRule.
    #Starts at 1 since the first line is reserved for the Configuration specifier. 
    method_specifier_line_number = 1
    queue_specifier_line_number = 2
    possible_routes_line_number = 3

    #Length of each specifier
    method_specifier_length = len(constants.ROUTING_RULE_METHOD_SPECIFIER)
    queue_specifier_length = len(constants.ROUTING_RULE_QUEUE_SPECIFIER)
    possible_routes_specifier_length = len(constants.ROUTING_RULE_POSSIBLE_ROUTES_SPECIFIER)
    
    if (len(template) - 1) % constants.ROUTING_RULE_COMMAND_LINES_COUNT > 0:
        return False

    while possible_routes_line_number <= len(template):
      change = self.config_change_request.routing_rule.Change()
      try:
        method_specifier = template[method_specifier_line_number][:method_specifier_length]
        queue_specifier = template[queue_specifier_line_number][:queue_specifier_length]
        possible_routes_specifier = template[possible_routes_line_number][:possible_routes_specifier_length]

        if method_specifier != constants.ROUTING_RULE_METHOD_SPECIFIER or queue_specifier != constants.ROUTING_RULE_QUEUE_SPECIFIER or \
           possible_routes_specifier != constants.ROUTING_RULE_POSSIBLE_ROUTES_SPECIFIER:
          return False
      except Exception:
        return False

      change.method = template[method_specifier_line_number][method_specifier_length:]
      change.queue = template[queue_specifier_line_number][queue_specifier_length:]
      change.possible_routes.extend(template[possible_routes_line_number][possible_routes_specifier_length:].split(", "))
      self.config_change_request.routing_rule.changes.append(change)
      
      method_specifier_line_number += constants.ROUTING_RULE_COMMAND_LINES_COUNT
      queue_specifier_line_number += constants.ROUTING_RULE_COMMAND_LINES_COUNT
      possible_routes_line_number += constants.ROUTING_RULE_COMMAND_LINES_COUNT

    return True

class QueueInfo(ConfigurationTypes):
  """Defines how QueueInfo templates should be parsed"""

  def parse_template(self, template):
    """Parses the template into a Protocol Buffer object that will
     be ready to send, given it is valid.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      bool: True if the comment was in valid template format.
      False if not in valid template format.
    """
    #These keep track of the current line number of each specifier for QueueInfo.
    #Starts at 1 since the first line is reserved for the Configuration specifier. 
    method_specifier_line_number = 1
    queue_specifier_line_number = 2
    owners_specifier_line_number = 3

    #Length of each specifier
    method_specifier_length = len(constants.QUEUE_INFO_METHOD_SPECIFIER)
    queue_specifier_length = len(constants.QUEUE_INFO_QUEUE_SPECIFIER)
    owners_specifier_length = len(constants.QUEUE_INFO_OWNERS_SPECIFIER)
    
    if (len(template) - 1) % constants.QUEUE_INFO_COMMAND_LINES_COUNT > 0:
        return False

    while owners_specifier_line_number <= len(template):
      change = self.config_change_request.queue_info.Change()
      try:
        method_specifier = template[method_specifier_line_number][:method_specifier_length]
        queue_specifier = template[queue_specifier_line_number][:queue_specifier_length]
        owners_specifier = template[owners_specifier_line_number][:owners_specifier_length]

        if method_specifier != constants.QUEUE_INFO_METHOD_SPECIFIER or queue_specifier != constants.QUEUE_INFO_QUEUE_SPECIFIER or\
           owners_specifier != constants.QUEUE_INFO_OWNERS_SPECIFIER:
          return False
      except Exception:
        return False

      change.method = template[method_specifier_line_number][method_specifier_length:]
      change.queue = template[queue_specifier_line_number][queue_specifier_length:]
      change.owners.extend(template[owners_specifier_line_number][owners_specifier_length:].split(", "))
      self.config_change_request.queue_info.changes.append(change)
      
      method_specifier_line_number += constants.QUEUE_INFO_COMMAND_LINES_COUNT
      queue_specifier_line_number += constants.QUEUE_INFO_COMMAND_LINES_COUNT
      owners_specifier_line_number += constants.QUEUE_INFO_COMMAND_LINES_COUNT

    return True
