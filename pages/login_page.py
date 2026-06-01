# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Actions ---
    def enter_username(self, username):
        self.type(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.type(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Complete login flow in one call."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # --- Queries ---
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_displayed(self.ERROR_MESSAGE)