# tests/test_inventory.py
import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import Config


@allure.feature("Inventory")
class TestInventory:

    @pytest.fixture(autouse=True)
    def login(self, driver):
        """
        This fixture runs automatically before every test in this class.
        'autouse=True' means no test needs to explicitly request it.
        Every inventory test starts already logged in.
        """
        login_page = LoginPage(driver)
        login_page.login(Config.STANDARD_USER, Config.PASSWORD)
        self.inventory = InventoryPage(driver)

    # -------------------------
    # Page Load Tests
    # -------------------------

    @allure.story("Page Load")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Inventory page loads after valid login")
    @pytest.mark.smoke
    def test_inventory_page_loads(self, driver):
        with allure.step("Verify URL contains inventory"):
            assert self.inventory.is_on_inventory_page(), (
                f"Expected inventory URL but got: {driver.current_url}"
            )

        with allure.step("Verify page title is 'Products'"):
            assert self.inventory.get_page_title() == "Products", (
                f"Expected 'Products' but got: {self.inventory.get_page_title()}"
            )

    @allure.story("Page Load")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Inventory page shows 6 products")
    @pytest.mark.regression
    def test_inventory_shows_six_products(self, driver):
        with allure.step("Count products on page"):
            count = self.inventory.get_product_count()
            assert count == 6, (
                f"Expected 6 products but found: {count}"
            )

    # -------------------------
    # Cart Tests
    # -------------------------

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Adding one item updates cart badge to 1")
    @pytest.mark.smoke
    def test_add_one_item_updates_cart_badge(self, driver):
        with allure.step("Verify cart is empty at start"):
            assert self.inventory.get_cart_count() == 0

        with allure.step("Add first product to cart"):
            self.inventory.add_item_to_cart_by_index(0)

        with allure.step("Verify cart badge shows 1"):
            assert self.inventory.get_cart_count() == 1, (
                f"Expected cart count 1 but got: {self.inventory.get_cart_count()}"
            )

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Adding multiple items updates cart badge correctly")
    @pytest.mark.regression
    def test_add_multiple_items_updates_cart_badge(self, driver):
        with allure.step("Add three products to cart"):
            self.inventory.add_item_to_cart_by_index(0)
            self.inventory.add_item_to_cart_by_index(1)
            self.inventory.add_item_to_cart_by_index(2)

        with allure.step("Verify cart badge shows 3"):
            assert self.inventory.get_cart_count() == 3, (
                f"Expected cart count 3 but got: {self.inventory.get_cart_count()}"
            )

    # -------------------------
    # Sort Tests
    # -------------------------

    @allure.story("Sort Products")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Products sort correctly by price low to high")
    @pytest.mark.regression
    def test_sort_by_price_low_to_high(self, driver):
        with allure.step("Sort products by price low to high"):
            self.inventory.sort_products_by("lohi")

        with allure.step("Verify prices are in ascending order"):
            prices = self.inventory.get_all_product_prices()
            assert prices == sorted(prices), (
                f"Prices not sorted correctly: {prices}"
            )

    @allure.story("Sort Products")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Products sort correctly by name A to Z")
    @pytest.mark.regression
    def test_sort_by_name_a_to_z(self, driver):
        with allure.step("Sort products by name A to Z"):
            self.inventory.sort_products_by("az")

        with allure.step("Verify product names are in alphabetical order"):
            names = self.inventory.get_all_product_names()
            assert names == sorted(names), (
                f"Names not sorted correctly: {names}"
            )

    # -------------------------
    # Navigation Tests
    # -------------------------

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Logout returns user to login page")
    @pytest.mark.regression
    def test_logout_redirects_to_login(self, driver):
        with allure.step("Click logout from burger menu"):
            self.inventory.logout()

        with allure.step("Verify redirected back to login page"):
            assert driver.current_url == Config.BASE_URL, (
                f"Expected login page but got: {driver.current_url}"
            )