"""This module is responsible for creating and publishing Protocol Buffer Objects via Pub/Sub
messages according to the configuration change request type specified in the template
submitted by the reporter of the Buganizer issue. It holds the Context, ConfigurationTypes,
EnqueueRule, RoutingRule, and QueueInfo classes and uses the strategy design pattern.
"""
from google.cloud import pubsub_v1
import constants
from config_change_request import config_type_pb2

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
        self.config_change_request = config_type_pb2.ConfigChangeRequest()
        self.config_change_request.reporter = reporter

    def publish(self):
        """Publish a message to a Pub/Sub topic.
        """
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(constants.PROJECT_ID, constants.TOPIC_NAME)
        data = self.config_change_request.SerializeToString()
        client.publish(topic_path, data=data)
        print("Message", self.config_change_type, "sent!")

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
        method_index = 1
        queue_index = 2
        features_index = 3
        priority_index = 4

        if len(template) < constants.ENQUEUE_RULE_COMMAND_LINES_COUNT + 1:
            return False

        while priority_index <= len(template):
            change = self.config_change_request.enqueue_rule.Change()
            try:
                method_specifier = template[method_index][:8]
                queue_specifier = template[queue_index][:7]
                features_specifier = template[features_index][:10]
                priority_specifier = template[priority_index][:10]

                if method_specifier != "Method: " or queue_specifier != "Queue: " or \
                features_specifier != "Features: " or priority_specifier != "Priority: ":
                    return False
            except Exception:
                return False

            method = template[method_index][8:]
            queue = template[queue_index][7:]
            features = template[features_index][10:]
            priority = template[priority_index][10:]

            change.method = method
            change.queue = queue
            change.priority = int(priority)
            for feature in features.split(", "):
                change.features.append(feature)

            self.config_change_request.enqueue_rule.changes.append(change)
            method_index += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
            queue_index += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
            features_index += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT
            priority_index += constants.ENQUEUE_RULE_COMMAND_LINES_COUNT

        return priority_index - constants.ENQUEUE_RULE_COMMAND_LINES_COUNT == len(template) - 1

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
        method_index = 1
        queue_index = 2
        possible_routes_index = 3

        if len(template) < constants.ROUTING_RULE_COMMAND_LINES_COUNT + 1:
            return False

        while possible_routes_index <= len(template):
            change = self.config_change_request.routing_rule.Change()
            try:
                method_specifier = template[method_index][:8]
                queue_specifier = template[queue_index][:7]
                possible_routes_specifier = template[possible_routes_index][:17]

                if method_specifier != "Method: " or queue_specifier != "Queue: " or \
                     possible_routes_specifier != "Possible-Routes: ":
                    return False
            except Exception:
                return False

            method = template[method_index][8:]
            queue = template[queue_index][7:]
            possible_routes = template[possible_routes_index][17:]

            change.method = method
            change.queue = queue
            for route in possible_routes.split(", "):
                change.possible_routes.append(route)

            self.config_change_request.routing_rule.changes.append(change)

            method_index += constants.ROUTING_RULE_COMMAND_LINES_COUNT
            queue_index += constants.ROUTING_RULE_COMMAND_LINES_COUNT
            possible_routes_index += constants.ROUTING_RULE_COMMAND_LINES_COUNT

        return possible_routes_index - constants.ROUTING_RULE_COMMAND_LINES_COUNT \
            == len(template) - 1

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
        method_index = 1
        queue_index = 2
        owners_index = 3

        if len(template) < constants.QUEUE_INFO_COMMAND_LINES_COUNT + 1:
            return False

        while owners_index <= len(template):
            change = self.config_change_request.queue_info.Change()
            try:
                method_specifier = template[method_index][:8]
                queue_specifier = template[queue_index][:7]
                owners_specifier = template[owners_index][:8]

                if method_specifier != "Method: " or queue_specifier != "Queue: " or\
                     owners_specifier != "Owners: ":
                    return False
            except Exception:
                return False

            method = template[method_index][8:]
            queue = template[queue_index][7:]
            owners = template[owners_index][8:]

            change.method = method
            change.queue = queue
            for owner in owners.split(", "):
                change.owner.append(owner)

            self.config_change_request.queue_info.changes.append(change)

            method_index += constants.QUEUE_INFO_COMMAND_LINES_COUNT
            queue_index += constants.QUEUE_INFO_COMMAND_LINES_COUNT
            owners_index += constants.QUEUE_INFO_COMMAND_LINES_COUNT

        return owners_index - constants.QUEUE_INFO_COMMAND_LINES_COUNT == len(template) - 1
