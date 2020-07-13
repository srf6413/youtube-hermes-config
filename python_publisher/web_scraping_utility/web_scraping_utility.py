"""This module holds the WebScrapingUtility class which does all Buganizer html scraping
  for issues under a componentid.
"""
import time
from bs4 import BeautifulSoup
from selenium import webdriver, common
from message_parsing_utility import message_parsing_utility
import constants

class WebScrapingUtility():
  """Responsible for all Buganizer html scraping."""
  def __init__(self, logger):
    """Setup the WebScrapingUtility

    Args:
        logger (logs.logger.Logger): the systems error logger
    """
    self.driver = self.setup_webdriver()
    self._message_parsing_util = message_parsing_utility.MessageParsingUtility(logger)
    self.logger = logger

  def setup_webdriver(self):
    """Completes all neccessary setup for the selenium web driver.

        Returns:
            selenium.webdriver.chrome.webdriver.WebDriver: the fully loaded Chrome
                                                          web driver with the desired profile.
    """
    try:
      options = webdriver.ChromeOptions()
      options.add_argument("user-data-dir=" + constants.PROFILE_PATH)
      driver = webdriver.Chrome(executable_path=constants.DRIVER_PATH,
                                options=options)
      return driver
    except common.exceptions.WebDriverException:
      error_message = "ERROR: Failed to load Chrome Driver. Check "\
        "path in constants.py and make sure there are no open windows with the desired profile.\n"
      self.logger.log(error_message)
      return None
    except Exception:
      return None

  def quit_scrape(self):
    """Terminate the webdriver.
    """
    if self.driver:
      self.driver.quit()
      self.driver = None

  def scrape_issues(self, url):
    """Opens the Buganizer url in the Chrome Browser and scrapes the webpage's source html
        to get the links for all the issues under the componentid.

        Args:
            url (str): the Buganizer url to scrape

        Return:
            list : List with all the buganizer issues found under the componentid.
    """
    try:
      self.driver.get(url)
    except common.exceptions.InvalidSessionIdException:
      self.driver.close()
      error_message = "ERROR: Failed to reach URL, check "\
      "specified URL in constants.py\n"
      self.logger.log(error_message)
      return []
    except Exception:
      self.driver.close()
      error_message = "ERROR: Failed to reach URL, check "\
      "specified URL in constants.py\n"
      self.logger.log(error_message)
      return []

    source_html = self.driver.page_source
    soup = BeautifulSoup(source_html, "html.parser")
    page_title = soup.title.string
    buganizer_issues = []

    if "Buganizer" not in page_title or "componentid" not in page_title:
      if "MOMA Single Sign On" in page_title:
        error_message = "ERROR: You must log into your MOMA account "\
        "first. Select the 'Use Security Code' option and generate a security code at go/sc.\n"\
          "Once you are logged in, close the browser and re-reun main.py\n"
        self.logger.log(error_message)

        while "Buganizer" not in page_title:
          source_html = self.driver.page_source
          soup = BeautifulSoup(source_html, "html.parser")
          page_title = soup.title.string
          time.sleep(1)

        return buganizer_issues
      error_message = "ERROR: URL does not link to a Buganizer "\
        "componentid, check specified URL "\
        "in constants.py\n"
      self.logger.log(error_message)
      return buganizer_issues

    for tbody in soup.find_all('tbody'):
      for _tr in tbody.find_all('tr'):
        issue_link = "https://b.corp.google.com/issues/" + _tr.get(
            'data-row-id')
        buganizer_issues.append(issue_link)
    return buganizer_issues

  def visit_all_issues_in_list(self, issues):
    """
    From the list of buganizer issues, visit each issue with the webdriver,
    find the reporter from an html tag send issue html to message_parsing_utility to be parsed.

    Args:
            issues (list): the Buganizer urls to scrape
    """
    for issue in issues:
      reporter = ""
      self.driver.get(issue)
      #Makes sure that page is fully loaded when grabbing the reporter tag
      while "@google.com" not in reporter:
        source_html = self.driver.page_source
        soup = BeautifulSoup(source_html, "html.parser")
        reporter_tag = soup.find("div", "bv2-issue-metadata-field-inner "\
          "bv2-issue-metadata-field-reporter")
        reporter = reporter_tag["aria-label"].replace(
            "Reporter value is ", "")

      self._message_parsing_util.parse_page(soup, reporter, issue)
