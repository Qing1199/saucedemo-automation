# tests/test_login.py
import pytest
import allure
from pages.login_page import LoginPage
from config import Config
from tests.test_data.login_data import INVALID_LOGIN_DATA


@allure.feature("Authentication")
class TestLogin:

    # -------------------------
    # Positive Tests
    # -------------------------

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User can login with valid credentials")
    @pytest.mark.smoke
    def test_valid_login(self, driver):
        with allure.step("Initialise login page"):
            login_page = LoginPage(driver)

        with allure.step("Enter valid credentials and click login"):
            login_page.login(Config.STANDARD_USER, Config.PASSWORD)

        with allure.step("Verify redirect to inventory page"):
            assert "test" in driver.current_url, (
                f"Expected invesntory page but got: {driver.current_url}"
            )

    # -------------------------
    # Negative Tests — Parametrized
    # -------------------------

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            (row[0], row[1], row[2])
            for row in INVALID_LOGIN_DATA
        ],
        ids=[row[3] for row in INVALID_LOGIN_DATA]   # readable test IDs
    )
    def test_invalid_login_shows_error(
        self, driver, username, password, expected_error
    ):
        # Dynamic title per scenario
        allure.dynamic.title(f"Invalid login: {username or 'empty'} / {password or 'empty'}")

        with allure.step(f"Enter username='{username}' password='{password}'"):
            login_page = LoginPage(driver)
            login_page.login(username, password)

        with allure.step(f"Verify error contains: '{expected_error}'"):
            assert login_page.is_error_displayed(), (
                "Expected error message to appear but it didn't"
            )
            assert expected_error in login_page.get_error_message(), (
                f"Expected '{expected_error}' but got: "
                f"'{login_page.get_error_message()}'"
            )