# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config


class BasePage:
    """
    Parent class for all Page Objects.
    Wraps Selenium actions into reusable, readable methods.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def find(self, locator):
        """Wait for element presence in DOM and return it."""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_clickable(self, locator):
        """Wait for element to be visible and clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        """Click an element safely — waits for clickability first."""
        self.find_clickable(locator).click()

    def type(self, locator, text):
        """Clear field and type text."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return visible text of an element."""
        return self.find(locator).text

    def is_displayed(self, locator):
        """Return True if element is visible, False otherwise."""
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def get_title(self):
        """Return current page title."""
        return self.driver.title

    def get_current_url(self):
        """Return current URL."""
        return self.driver.current_url