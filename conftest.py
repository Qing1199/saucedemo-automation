# conftest.py
import pytest
import allure
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

logging.getLogger('WDM').setLevel(logging.NOTSET)


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()

    # Auto-detect CI environment and enable headless
    # GitHub Actions sets CI=true automatically
    if os.getenv("CI"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        # Local — show browser so you can watch tests run
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    # Disable password manager popups
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.maximize_window()
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    driver.get(Config.BASE_URL)

    yield driver

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )