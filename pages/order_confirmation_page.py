# pages/order_confirmation_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrderConfirmationPage(BasePage):

    CONFIRMATION_HEADER  = (By.CLASS_NAME, "complete-header")
    CONFIRMATION_TEXT    = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BTN        = (By.ID, "back-to-products")

    # --- Actions ---
    def click_back_home(self):
        """Return to inventory page after order."""
        self.click(self.BACK_HOME_BTN)

    # --- Queries ---
    def get_confirmation_header(self):
        """Returns 'Thank you for your order!'"""
        return self.get_text(self.CONFIRMATION_HEADER)

    def get_confirmation_text(self):
        """Returns the order dispatch message."""
        return self.get_text(self.CONFIRMATION_TEXT)

    def is_order_confirmed(self):
        """True if confirmation header is visible."""
        return self.is_displayed(self.CONFIRMATION_HEADER)

    def is_on_confirmation_page(self):
        return "checkout-complete" in self.get_current_url()