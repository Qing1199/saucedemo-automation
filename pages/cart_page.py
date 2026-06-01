# pages/cart_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    PAGE_TITLE       = (By.CLASS_NAME, "title")
    CART_ITEMS       = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES       = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES      = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON  = (By.ID, "checkout")
    CONTINUE_BUTTON  = (By.ID, "continue-shopping")
    REMOVE_BUTTON    = (By.CSS_SELECTOR, "[data-test^='remove']")

    # --- Actions ---
    def click_checkout(self):
        """Proceed to checkout form."""
        self.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
        """Go back to inventory page."""
        self.click(self.CONTINUE_BUTTON)

    def remove_first_item(self):
        """Remove the first item in the cart."""
        buttons = self.driver.find_elements(*self.REMOVE_BUTTON)
        if buttons:
            buttons[0].click()

    # --- Queries ---
    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_cart_items(self):
        """Return list of all cart item WebElements."""
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_cart_item_count(self):
        """Return number of items currently in cart."""
        return len(self.get_cart_items())

    def get_item_names(self):
        """Return list of item name strings in cart."""
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_item_prices(self):
        """Return list of item prices as floats."""
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    def is_on_cart_page(self):
        return "cart" in self.get_current_url()