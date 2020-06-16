"""Test file for the Buganizer web-scraper."""
from io import StringIO
from unittest.mock import patch
import unittest
import main
import constants
from web_utils import web_utils

class TestsMain(unittest.TestCase):
    """Test methods from main.py

    Args:
        unittest (unittest.TestCase): unittest Testcase
    """
    def test_begin_scrape(self):
        """Test begin_scrape with buganizer link. Assert that program sends messages via pubsub.
        """
        system = main.System()
        url = "https://b.corp.google.com/issues?q=componentid:889136"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            system.begin_scrape(url)

            assert "Message" in fake_out.getvalue() and "sent!" in fake_out.getvalue()

    def test_begin_scrape_non_buganizer(self):
        """Test begin_scrape with non-buganizer link.
        Assert that program returns proper alert message.
        """
        system = main.System()
        url = "https://www.google.com"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            system.begin_scrape(url)
            assert "ERROR: URL does not link to a Buganizer componentid, check "\
                "specified URL in constants.py" in fake_out.getvalue()
        system.quit_scrape()

    def test_begin_scrape_bogus(self):
        """Test begin_scrape with non-buganizer link.
        Assert that program returns proper alert message.
        """
        system = main.System()
        url = "djhgfjhgfjddfhg"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            system.begin_scrape(url)
            assert "ERROR: Failed to reach URL, check specified URL "\
                "in constants.py" in fake_out.getvalue()
        system.quit_scrape()

class TestsWebUtils(unittest.TestCase):
    """Test methods from web_utils.py

    Args:
        unittest (unittest.TestCase): unittest Testcase
    """
    def test_visit_all_issues_setup(self):
        """Try to run scrape_issues with bad driver path.
        Assert that program returns proper alert message.
        """
        web_driver = web_utils.WebUtils()
        constants.DRIVER_PATH = ""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            web_driver.scrape_issues("https://b.corp.google.com/issues?q=componentid:889136")
            assert "ERROR: Failed to load Chrome Driver. Check path in "\
                "constants.py" in fake_out.getvalue()

    def test_quit_scrape(self):
        """Test quit_scrape when driver has not been set up.
        Assert that program returns proper alert message.
        """
        web_driver = web_utils.WebUtils()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            web_driver.quit_scrape()
            assert "ERROR: Driver does is not setup." in fake_out.getvalue()

    def test_visit_all_issues_not_setup(self):
        """Test visit_all_issues if scrape_issues has not yet been called.
        Assert that program returns proper alert message.
        """
        web_driver = web_utils.WebUtils()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            web_driver.visit_all_issues()
            assert "ERROR: Buganizer has not gathered issues and is attempting "\
                "to visit them." in fake_out.getvalue()

if __name__ == '__main__':
    unittest.main()
