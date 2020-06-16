"""This module holds the System class which completes any necessary setup for scraping.
"""
import sys
import constants
sys.path.insert(1, constants.PROJECT_PATH)
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
        success = self._web_util.scrape_issues(url)
        if success:
            self._web_util.visit_all_issues()

    def quit_scrape(self):
        """Quit the proccess of scraping Buganizer.

        Args:
            url (str): the Buganizer url to scrape
        """
        self._web_util.quit_scrape()

if __name__ == "__main__":
    system = System()
    system.begin_scrape(constants.URL)
