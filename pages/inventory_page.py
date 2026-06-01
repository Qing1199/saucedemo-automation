# pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):

    # --- Locators ---
    PAGE_TITLE      = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES     = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE      = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON       = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN   = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU     = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK     = (By.ID, "logout_sidebar_link")

    # --- Actions ---
    def add_item_to_cart_by_index(self, index=0):
        """Add product by position — 0 = first product."""
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BTN)
        buttons[index].click()

    def add_item_to_cart_by_name(self, product_name):
        """Add a specific product by its exact display name."""
        locator = (
            By.CSS_SELECTOR,
            f"[data-test='add-to-cart-{product_name.lower().replace(' ', '-')}']"
        )
        self.click(locator)

    def sort_products_by(self, option):
        """Sort products. Options: 'az', 'za', 'lohi', 'hilo'"""
        dropdown = self.find(self.SORT_DROPDOWN)
        select = Select(dropdown)
        select.select_by_value(option)

    def go_to_cart(self):
        """Navigate to cart page."""
        self.click(self.CART_ICON)

    def logout(self):
        """Logout via burger menu."""
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)

    # --- Queries ---
    def get_page_title(self):
        """Return page heading text."""
        return self.get_text(self.PAGE_TITLE)

    def get_all_product_names(self):
        """Return list of all product name strings."""
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_all_product_prices(self):
        """Return list of product prices as floats."""
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    def get_cart_count(self):
        """Return cart item count — 0 if empty."""
        try:
            return int(self.get_text(self.CART_BADGE))
        except Exception:
            return 0

    def get_product_count(self):
        """Return total number of products on page."""
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def is_on_inventory_page(self):
        """Return True if current URL contains 'inventory'."""
        return "inventory" in self.get_current_url()