# pages/products_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    # --- Locators ---
    PAGE_TITLE       = (By.CLASS_NAME, "title")
    ADD_TO_CART_BTN  = (By.CSS_SELECTOR, "[data-test='add-to-cart-sauce-labs-backpack']")
    CART_BADGE       = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON        = (By.CLASS_NAME, "shopping_cart_link")

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def add_backpack_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        self.click(self.CART_ICON)