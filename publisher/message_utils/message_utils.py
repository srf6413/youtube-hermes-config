"""This module holds the MessageUtils class which parses the source html and the
reporters comments on a given issue.
"""
from config_change_request import config_change_request

class MessageUtils():
  """Responsible for parsing the source html and the
  reporters comments on a given issue"""

  def parse_page(self, soup, reporter):
    """Parses the source html for the reporter and their comments from each
    of the issues under the given componentid. Once each comment is scraped, the message
    and reporter are sent to generate_message().
    Args:
      soup (BeautifulSoup): the BeautifulSoup object of the Buganizer issue
      reporter (str): the reporter of the Buganizer issue
    """
    comments = soup.find_all("li", "bv2-event ng-star-inserted")

    for user_comment in comments:
      current_user = user_comment.find("span", "bv2-event-user-id")['data-hovercard-id']
      if current_user == reporter:
        comment_text_tag = user_comment.find("b-plain-format-unquoted-section",
                           "ng-star-inserted")
        if comment_text_tag is not None:
          comment = comment_text_tag.get_text(separator='\n')
          self.generate_message(reporter, comment)

  def generate_message(self, reporter, comment):
    """Splits the reporter's comment and extracts all configuration change request.
    Createsa ConfigChangeRequest Proto Buf object in accordance to what the template
    specifies, so it can be seamlessly published by Pub/Sub.

    Args:
      reporter (str): the reporter of the current Buganizer issue
      comment (str): the reporter's comment on the current Buganizer issue
    """
    template = comment.splitlines()
    config_specifier = template[0][:15]
    config_change_type = template[0][15:]
    if config_specifier != "Configuration: ":
      return

    if config_change_type == "EnqueueRule":
      config_change_type = config_change_request.EnqueueRule(reporter, config_change_type)
      context = config_change_request.Context(config_change_type)
      template_complete = context.prepare_for_publish(template)

      if template_complete:
        context.pub()
    elif config_change_type == "RoutingRule":
      config_change_type = config_change_request.RoutingRule(reporter, config_change_type)
      context = config_change_request.Context(config_change_type)
      template_complete = context.prepare_for_publish(template)

      if template_complete:
        context.pub()
    elif config_change_type == "QueueInfo":
      config_change_type = config_change_request.QueueInfo(reporter, config_change_type)
      context = config_change_request.Context(config_change_type)
      template_complete = context.prepare_for_publish(template)

      if template_complete:
        context.pub()
    else:
      return
