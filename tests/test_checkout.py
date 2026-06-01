# tests/test_checkout.py
import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage
from config import Config
from tests.test_data.checkout_data import VALID_CUSTOMER, INVALID_CHECKOUT_DATA


@allure.feature("Checkout")
class TestCheckout:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Login and add one item to cart before every checkout test.
        All checkout tests need at least one item in cart to proceed.
        """
        # Login
        login_page = LoginPage(driver)
        login_page.login(Config.STANDARD_USER, Config.PASSWORD)

        # Add one item to cart
        self.inventory = InventoryPage(driver)
        self.inventory.add_item_to_cart_by_index(0)

        # Go to cart
        self.inventory.go_to_cart()

        # Initialise all page objects — driver is shared
        self.cart     = CartPage(driver)
        self.checkout = CheckoutPage(driver)
        self.confirm  = OrderConfirmationPage(driver)

    # -------------------------
    # Cart Verification Tests
    # -------------------------

    @allure.story("Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Cart contains correct item after adding from inventory")
    @pytest.mark.smoke
    def test_cart_contains_added_item(self, driver):
        with allure.step("Verify cart page loaded"):
            assert self.cart.is_on_cart_page(), (
                f"Expected cart URL but got: {driver.current_url}"
            )

        with allure.step("Verify exactly one item in cart"):
            assert self.cart.get_cart_item_count() == 1, (
                f"Expected 1 item but found: {self.cart.get_cart_item_count()}"
            )

    @allure.story("Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Removing item from cart empties the cart")
    @pytest.mark.regression
    def test_remove_item_from_cart(self, driver):
        with allure.step("Verify one item in cart"):
            assert self.cart.get_cart_item_count() == 1

        with allure.step("Remove item from cart"):
            self.cart.remove_first_item()

        with allure.step("Verify cart is now empty"):
            assert self.cart.get_cart_item_count() == 0, (
                "Expected cart to be empty after removal"
            )

    # -------------------------
    # Happy Path E2E Test
    # -------------------------

    @allure.story("Complete Purchase")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User can complete full checkout flow successfully")
    @pytest.mark.smoke
    def test_complete_checkout_flow(self, driver):
        with allure.step("Click checkout from cart"):
            self.cart.click_checkout()
            assert self.checkout.is_on_step_one(), (
                f"Expected checkout step one but got: {driver.current_url}"
            )

        with allure.step("Fill customer information form"):
            self.checkout.complete_checkout(
                VALID_CUSTOMER["first_name"],
                VALID_CUSTOMER["last_name"],
                VALID_CUSTOMER["postal_code"]
            )

        with allure.step("Verify order summary page loads"):
            assert self.checkout.is_on_step_two(), (
                f"Expected checkout step two but got: {driver.current_url}"
            )

        with allure.step("Verify total = subtotal + tax"):
            subtotal = self.checkout.get_subtotal()
            tax      = self.checkout.get_tax()
            total    = self.checkout.get_total()
            expected_total = round(subtotal + tax, 2)

            assert total == expected_total, (
                f"Total ${total} does not match subtotal ${subtotal} + tax ${tax}"
            )

        with allure.step("Click finish to place order"):
            self.checkout.click_finish()

        with allure.step("Verify order confirmation page"):
            assert self.confirm.is_on_confirmation_page(), (
                f"Expected confirmation page but got: {driver.current_url}"
            )
            assert self.confirm.is_order_confirmed(), (
                "Confirmation header not visible"
            )
            assert "Thank you" in self.confirm.get_confirmation_header(), (
                f"Unexpected header: {self.confirm.get_confirmation_header()}"
            )

    # -------------------------
    # Checkout Form Validation
    # -------------------------

    @allure.story("Checkout Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Checkout form shows error when required fields missing")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "first_name, last_name, postal_code, expected_error",
        [
            (row[0], row[1], row[2], row[3])
            for row in INVALID_CHECKOUT_DATA
        ],
        ids=[row[4] for row in INVALID_CHECKOUT_DATA]
    )
    def test_checkout_form_validation(
        self, driver, first_name, last_name, postal_code, expected_error
    ):
        allure.dynamic.title(f"Checkout form error: {expected_error}")

        with allure.step("Navigate to checkout step one"):
            self.cart.click_checkout()

        with allure.step(f"Submit form with missing field"):
            self.checkout.fill_customer_info(
                first_name, last_name, postal_code
            )
            self.checkout.click_continue()

        with allure.step(f"Verify error: '{expected_error}'"):
            assert self.checkout.is_error_displayed(), (
                "Expected validation error but none appeared"
            )
            assert expected_error in self.checkout.get_error_message(), (
                f"Expected '{expected_error}' but got: "
                f"'{self.checkout.get_error_message()}'"
            )

    # -------------------------
    # Post-Order Navigation
    # -------------------------

    @allure.story("Complete Purchase")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Back to products button returns to inventory after order")
    @pytest.mark.regression
    def test_back_to_products_after_order(self, driver):
        with allure.step("Complete full checkout"):
            self.cart.click_checkout()
            self.checkout.complete_checkout(
                VALID_CUSTOMER["first_name"],
                VALID_CUSTOMER["last_name"],
                VALID_CUSTOMER["postal_code"]
            )
            self.checkout.click_finish()

        with allure.step("Verify on confirmation page"):
            assert self.confirm.is_on_confirmation_page()

        with allure.step("Click back to products"):
            self.confirm.click_back_home()

        with allure.step("Verify returned to inventory page"):
            assert self.inventory.is_on_inventory_page(), (
                f"Expected inventory but got: {driver.current_url}"
            )