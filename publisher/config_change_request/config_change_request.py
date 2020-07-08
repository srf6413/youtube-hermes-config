"""This module is responsible for creating and publishing Protocol Buffer Objects via Pub/Sub
messages according to the configuration change request type specified in the template
submitted by the reporter of the Buganizer issue. It holds the Context, ConfigurationTypes,
EnqueueRule, RoutingRule, and QueueInfo classes and uses the factory design pattern.
"""
from datetime import datetime
from google.cloud import pubsub_v1
from publisher import constants
from publisher.config_change_request import config_change_pb2

class ConfigurationTypeFactory():
  """The Facory for making the different types of configurations
  (EnqueueRule, RoutingRule, QueueInfo)
  """

  def __init__(self, reporter, config_change_type, issue, comment):
    """Initialize the ConfigurationTypeFactory

    Args:
        reporter (str): the reporter of the current Buganizer issue
        config_change_type (str): the type of configuraiton (EnqueueRule, RoutingRule, QueueInfo)
        issue (str): the URL of the current Buganizer issue
        comment (str): the reporter's comment on the current Buganizer issue
    """
    self.config_change_type = config_change_type
    self.config_change_request = config_change_pb2.ConfigChangeRequest()
    self.config_change_request.reporter = reporter
    self.issue = issue
    self.comment = comment

  def make_enqueue_rule(self, template):
    """Parses the template into a ConfigChangeRequest object that will
     be ready to send, given it is valid.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      ConfigChangeRequest: The config change request object containing either the complete
      Proto Buf object or no Proto Buf object and a detailed error message for logging.

    """
    config_change_request = ConfigurationChangeRequest()
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

    #This checks that the template is the correct number of lines long
    if (len(template) - 1) % constants.ENQUEUE_RULE_COMMAND_LINES_COUNT > 0:
      error = str(datetime.now()) + "  The following configuration change request from " + \
      self.issue + " is invalid. The number of lines does not match for a correct EnqueueRule "\
        "template. Please check that the format correctly matches template and try again.\n" + \
      self.comment + "\n"
      config_change_request.error_message = error
      return config_change_request

    for line_idx in range(1, len(template), constants.ENQUEUE_RULE_COMMAND_LINES_COUNT):

      method_specifier_line_number, queue_specifier_line_number, features_specifier_line_number, \
             priority_specifier_line_number = (
                 range(line_idx, line_idx + constants.ENQUEUE_RULE_COMMAND_LINES_COUNT))

      change = self.config_change_request.enqueue_rule.Change()

      method_specifier = template[method_specifier_line_number][:method_specifier_length]
      queue_specifier = template[queue_specifier_line_number][:queue_specifier_length]
      features_specifier = template[features_specifier_line_number][:features_specifier_length]
      priority_specifier = template[priority_specifier_line_number][:priority_specifier_length]

      if method_specifier != constants.ENQUEUE_RULE_METHOD_SPECIFIER or queue_specifier != \
        constants.ENQUEUE_RULE_QUEUE_SPECIFIER or features_specifier != \
          constants.ENQUEUE_RULE_FEATURES_SPECIFIER or priority_specifier != \
            constants.ENQUEUE_RULE_PRIORITY_SPECIFIER:
        error = str(datetime.now()) + "  The following configuration change request from " + \
        self.issue + " is invalid. One or more specifiers are not correct for a EnqueueRule "\
        "template. Please check that the format correctly matches template and try again.\n" + \
        self.comment + "\n"
        config_change_request.error_message = error
        return config_change_request


      change.method = template[method_specifier_line_number][method_specifier_length:]
      change.queue = template[queue_specifier_line_number][queue_specifier_length:]
      change.features.extend(template[features_specifier_line_number][features_specifier_length:].\
        split(", "))
      change.priority = int(template[priority_specifier_line_number][priority_specifier_length:])
      self.config_change_request.enqueue_rule.changes.append(change)

    config_change_request.proto = self.config_change_request
    return config_change_request


  def make_routing_rule(self, template):
    """Parses the template into a ConfigChangeRequest object that will be ready to send,
    given it is valid.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      ConfigChangeRequest: The config change request object containing either the complete
      Proto Buf object or no Proto Buf object and a detailed error message for logging.
    """
    config_change_request = ConfigurationChangeRequest()
    #These keep track of the current line number of each specifier for RoutingRule.
    #Starts at 1 since the first line is reserved for the Configuration specifier.
    method_specifier_line_number = 1
    queue_specifier_line_number = 2
    possible_routes_specifier_line_number = 3

    #Length of each specifier
    method_specifier_length = len(constants.ROUTING_RULE_METHOD_SPECIFIER)
    queue_specifier_length = len(constants.ROUTING_RULE_QUEUE_SPECIFIER)
    possible_routes_specifier_length = len(constants.ROUTING_RULE_POSSIBLE_ROUTES_SPECIFIER)

    #This checks that the template is the correct number of lines long
    if (len(template) - 1) % constants.ROUTING_RULE_COMMAND_LINES_COUNT > 0:
      error = str(datetime.now()) + "  The following configuration change request from " + \
      self.issue + " is invalid. The number of lines does not match for a correct RoutingRule "\
      "template. Please check that the format correctly matches template and try again.\n" + \
      self.comment + "\n"
      config_change_request.error_message = error
      return config_change_request

    for line_idx in range(1, len(template), constants.ROUTING_RULE_COMMAND_LINES_COUNT):

      method_specifier_line_number, queue_specifier_line_number,\
      possible_routes_specifier_line_number = (range(line_idx, line_idx +
                                                     constants.ROUTING_RULE_COMMAND_LINES_COUNT))

      change = self.config_change_request.routing_rule.Change()

      method_specifier = template[method_specifier_line_number][:method_specifier_length]
      queue_specifier = template[queue_specifier_line_number][:queue_specifier_length]
      possible_routes_specifier = template[possible_routes_specifier_line_number]\
      [:possible_routes_specifier_length]

      if method_specifier != constants.ROUTING_RULE_METHOD_SPECIFIER or queue_specifier != \
      constants.ROUTING_RULE_QUEUE_SPECIFIER or possible_routes_specifier != \
      constants.ROUTING_RULE_POSSIBLE_ROUTES_SPECIFIER:
        error = str(datetime.now()) + "  The following configuration change request from " + \
        self.issue + " is invalid. One or more specifiers are not correct for a RoutingRule "\
        "template. Please check that the format correctly matches template and try again.\n" + \
        self.comment + "\n"
        config_change_request.error_message = error
        return config_change_request

      change.method = template[method_specifier_line_number][method_specifier_length:]
      change.queue = template[queue_specifier_line_number][queue_specifier_length:]
      change.possible_routes.extend(template[possible_routes_specifier_line_number]\
     [possible_routes_specifier_length:].split(", "))
      self.config_change_request.routing_rule.changes.append(change)

    config_change_request.proto = self.config_change_request
    return config_change_request

  def make_queue_info(self, template):
    """Parses the template into a ConfigChangeRequest object that will
     be ready to send, given it is valid.

    Args:
      template (str): the reporters comment of the configuration template

    Returns:
      ConfigChangeRequest: The config change request object containing either the complete
      Proto Buf object or no Proto Buf object and a detailed error message for logging.
    """
    config_change_request = ConfigurationChangeRequest()
    #These keep track of the current line number of each specifier for QueueInfo.
    #Starts at 1 since the first line is reserved for the Configuration specifier.
    method_specifier_line_number = 1
    queue_specifier_line_number = 2
    owners_specifier_line_number = 3

    #Length of each specifier
    method_specifier_length = len(constants.QUEUE_INFO_METHOD_SPECIFIER)
    queue_specifier_length = len(constants.QUEUE_INFO_QUEUE_SPECIFIER)
    owners_specifier_length = len(constants.QUEUE_INFO_OWNERS_SPECIFIER)

    #This checks that the template is the correct number of lines long
    if (len(template) - 1) % constants.QUEUE_INFO_COMMAND_LINES_COUNT > 0:
      error = str(datetime.now()) + "  The following configuration change request from " + \
      self.issue + " is invalid. The number of lines does not match for a correct QueueInfo "\
      "template. Please check that the format correctly matches template and try again.\n" + \
      self.comment + "\n"
      config_change_request.error_message = error
      return config_change_request

    for line_idx in range(1, len(template), constants.QUEUE_INFO_COMMAND_LINES_COUNT):

      method_specifier_line_number, queue_specifier_line_number, owners_specifier_line_number = (
          range(line_idx, line_idx + constants.QUEUE_INFO_COMMAND_LINES_COUNT))

      change = self.config_change_request.queue_info.Change()
      method_specifier = template[method_specifier_line_number][:method_specifier_length]
      queue_specifier = template[queue_specifier_line_number][:queue_specifier_length]
      owners_specifier = template[owners_specifier_line_number][:owners_specifier_length]

      if method_specifier != constants.QUEUE_INFO_METHOD_SPECIFIER or queue_specifier != \
      constants.QUEUE_INFO_QUEUE_SPECIFIER or owners_specifier != \
      constants.QUEUE_INFO_OWNERS_SPECIFIER:
        error = str(datetime.now()) + "  The following configuration change request from " + \
        self.issue + " is invalid. One or more specifiers are not correct for a QueueInfo "\
        "template. Please check that the format correctly matches template and try again.\n" + \
        self.comment + "\n"
        config_change_request.error_message = error
        return config_change_request

      change.method = template[method_specifier_line_number][method_specifier_length:]
      change.queue = template[queue_specifier_line_number][queue_specifier_length:]
      change.owners.extend(template[owners_specifier_line_number][owners_specifier_length:].split(\
        ", "))
      self.config_change_request.queue_info.changes.append(change)

    config_change_request.proto = self.config_change_request
    return config_change_request

  def publish(self, config_change_request):
    """Publishes a message to a Pub/Sub topic.
    """
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(constants.PROJECT_ID, constants.TOPIC_NAME)
    data = config_change_request.SerializeToString()
    client.publish(topic_path, data=data)

class ConfigurationChangeRequest():
  """A wrapper object to hold configuration change request Proto Buf objects
  or a error message if neccessary.
  """
  def __init__(self):
    self.proto = None
    self.error_message = ""
