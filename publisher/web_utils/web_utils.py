"""This module holds the WebUtils class which does all Buganizer html scraping
  for issues under a componentid.
"""
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from message_utils import message_utils
import constants


class WebUtils():
  """Responsible for all Buganizer html scraping."""
  def __init__(self):
    self._driver = None
    self._message_util = message_utils.MessageUtils()

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
      self._driver = driver
      return True
    except Exception:
      print("ERROR: Failed to load Chrome Driver. Check path in constants.py"\
        " and make sure there are no open windows with the desired profile")
      return False

  def quit_scrape(self):
    """Terminate the webdriver.
        """
    if self._driver is not None:
      self._driver.quit()
      self._driver = None
    else:
      print("ERROR: Driver does is not setup.")

  def scrape_issues(self, url):
    """Opens the Buganizer url in the Chrome Browser and scrapes the webpage's source html
        to get the links for all the issues under the componentid.

        Args:
            url (str): the Buganizer url to scrape

        Return:
            list : List with all the buganizer issues found under the componentid.
        """
    buganizer_issues = []
    if not self.setup_webdriver():
      return buganizer_issues

    try:
      self._driver.get(url)
    except Exception:
      self._driver.close()
      print(
          "ERROR: Failed to reach URL, check specified URL in constants.py"
      )
      return buganizer_issues

    source_html = self._driver.page_source
    soup = BeautifulSoup(source_html, "html.parser")
    page_title = soup.title.string

    if "Buganizer" not in page_title or "componentid" not in page_title:
      if "MOMA Single Sign On" in page_title:
        print("ERROR: You must log into your MOMA account first. Select the "\
          "'Use Security Code' option and generate a security code at go/sc.\n"\
          "Once you are logged in, close the browser and re-reun main.py")
        while "Buganizer" not in page_title:
          source_html = self._driver.page_source
          soup = BeautifulSoup(source_html, "html.parser")
          page_title = soup.title.string
          time.sleep(1)
        print(
            "Close browser window and restart program now that you are logged in."
        )
        return buganizer_issues
      print("ERROR: URL does not link to a Buganizer componentid, check specified URL "\
        "in constants.py")
      return buganizer_issues

    for tbody in soup.find_all('tbody'):
      for _tr in tbody.find_all('tr'):
        issue_link = "https://b.corp.google.com/issues/" + _tr.get(
            'data-row-id')
        buganizer_issues.append(issue_link)
    return buganizer_issues

  def visit_all_issues(self, issues):
    """
    From the list of buganizer issues, visit each issue and
        send to message_utils to be parsed.
        
    Args:
            issues (list): the Buganizer urls to scrape 
    """
    for issue in issues:
      reporter = "empty"
      self._driver.get(issue)
      while "@google.com" not in reporter:
        source_html = self._driver.page_source
        soup = BeautifulSoup(source_html, "html.parser")
        reporter_tag = soup.find("div", "bv2-issue-metadata-field-inner "\
          "bv2-issue-metadata-field-reporter")
        reporter = reporter_tag["aria-label"].replace(
            "Reporter value is ", "")

      self._message_util.parse_page(soup, reporter)
    self.quit_scrape()
