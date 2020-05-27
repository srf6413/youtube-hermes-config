"""This module holds the System class which completes any necessary setup for scraping.
"""
import constants
from web_utils import web_utils

class System():
  """Completes any necessary setup for scraping."""

  def __init__(self):
    self._web_util = web_utils.WebUtils()

  def begin_scrape(self, url):
    """Begins the proccess of scraping Buganizer.

    Args:
      url (str): the Buganizer url to scrape
    """
    while True:
      issues = self._web_util.scrape_issues(url)

      if len(issues) > 0:
          self._web_util.visit_all_issues(issues)

if __name__ == "__main__":
  system = System()
  system.begin_scrape(constants.URL)
