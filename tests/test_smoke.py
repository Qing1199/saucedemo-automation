# tests/test_smoke.py
def test_browser_opens(driver):           # <-- "driver" matches the fixture name exactly
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title
    print(f"\nPage title: {driver.title}")