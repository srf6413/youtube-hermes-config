"""This module holds the MessageUtils class which parses the source html and the
reporters comments on a given issue.
"""
from publisher import constants
from publisher.config_change_request import config_change_request
from publisher.logs.global_logger import logger

class MessageUtils():
  """Responsible for parsing the source html and the
  reporters comments on a given issue"""

  def __init__(self):
    self.issue_comments_counts = {}

  def parse_page(self, soup, reporter, issue):
    """Parses the source html for the reporter and their comments from each
    of the issues under the given componentid. Once each comment is scraped, the message
    and reporter are sent to generate_message().
    Args:
      soup (BeautifulSoup): the BeautifulSoup object of the Buganizer issue
      reporter (str): the reporter of the Buganizer issue
      issue (str): the URL of the current Buganizer issue
    """
    comments = soup.find_all("li", "bv2-event ng-star-inserted")
    current_comments_count = len(comments)

    if issue not in self.issue_comments_counts.keys():
      self.issue_comments_counts[issue] = 0

    if current_comments_count > self.issue_comments_counts[issue]:
      for i in range(self.issue_comments_counts[issue], current_comments_count):
        user_comment = comments[i]
        current_user = user_comment.find("span", "bv2-event-user-id")['data-hovercard-id']
        if current_user == reporter:
          comment_text_tag = user_comment.find("b-plain-format-unquoted-section",
                                               "ng-star-inserted")
          if comment_text_tag is not None:
            comment = comment_text_tag.get_text(separator='\n')
            self.generate_message(reporter, comment, issue)
      self.issue_comments_counts[issue] = current_comments_count

  def generate_message(self, reporter, comment, issue):
    """Splits the reporter's comment and extracts all configuration change request.
    Creates a ConfigChangeRequest Proto Buf object depending on the type of template
    and is seamlessly published by Pub/Sub.

    Args:
      reporter (str): the reporter of the current Buganizer issue
      comment (str): the reporter's comment on the current Buganizer issue
      issue (str): the URL of the current Buganizer issue
    """
    template = comment.splitlines()
    config_specifier_length = len(constants.CONFIGURATION_SPECIFIER)
    config_specifier = template[0][:config_specifier_length]
    config_change_type = template[0][config_specifier_length:]
    if config_specifier != "Configuration: ":
      return

    factory = config_change_request.ConfigurationTypeFactory(reporter, config_change_type,
                                                             issue, comment)
    if config_change_type == "EnqueueRule":
      config_change = factory.make_enqueue_rule(template)
    elif config_change_type == "RoutingRule":
      config_change = factory.make_routing_rule(template)
    elif config_change_type == "QueueInfo":
      config_change = factory.make_queue_info(template)
    else:
      return

    #This means template was valid and ready to send
    if config_change.proto is not None:
      factory.publish(config_change.proto)
    #Otherwise log what the problem with the template was
    else:
      logger.info(config_change.error_message)
      return
