# pages/checkout_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Page Object for Checkout Step One (form) and Step Two (summary).
    Step One URL: https://www.saucedemo.com/checkout-step-one.html
    Step Two URL: https://www.saucedemo.com/checkout-step-two.html
    """

    # --- Step One Locators (Info Form) ---
    PAGE_TITLE      = (By.CLASS_NAME, "title")
    FIRST_NAME      = (By.ID, "first-name")
    LAST_NAME       = (By.ID, "last-name")
    POSTAL_CODE     = (By.ID, "postal-code")
    CONTINUE_BTN    = (By.ID, "continue")
    CANCEL_BTN      = (By.ID, "cancel")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Step Two Locators (Order Summary) ---
    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX      = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL    = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN       = (By.ID, "finish")

    # --- Step One Actions ---
    def fill_customer_info(self, first_name, last_name, postal_code):
        """Fill in the checkout form fields."""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)

    def click_continue(self):
        """Submit the form — move to order summary."""
        self.click(self.CONTINUE_BTN)

    def click_cancel(self):
        """Cancel and go back to cart."""
        self.click(self.CANCEL_BTN)

    def click_finish(self):
        """Place the order — move to confirmation page."""
        self.click(self.FINISH_BTN)

    def complete_checkout(self, first_name, last_name, postal_code):
        """Fill form and continue — one convenient method."""
        self.fill_customer_info(first_name, last_name, postal_code)
        self.click_continue()

    # --- Step One Queries ---
    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_displayed(self.ERROR_MESSAGE)

    # --- Step Two Queries ---
    def get_subtotal(self):
        """Return subtotal as float — strips 'Item total: $' prefix."""
        text = self.get_text(self.SUMMARY_SUBTOTAL)
        return float(text.split("$")[1])

    def get_tax(self):
        """Return tax as float."""
        text = self.get_text(self.SUMMARY_TAX)
        return float(text.split("$")[1])

    def get_total(self):
        """Return order total as float."""
        text = self.get_text(self.SUMMARY_TOTAL)
        return float(text.split("$")[1])

    def is_on_step_one(self):
        return "checkout-step-one" in self.get_current_url()

    def is_on_step_two(self):
        return "checkout-step-two" in self.get_current_url()