import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestCase01:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def test_url_is_valid(self):
        driver = self.driver

        # Navigate to the URL
        driver.get("https://www.guvi.in")


        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Validate current URL contains guvi.in
        current_url = driver.current_url
        assert "guvi.in" in current_url, f"FAIL: Unexpected URL — '{current_url}'"

        # Validate HTTP response
        page_source = driver.page_source
        assert len(page_source) > 100, "FAIL: Page source is too short — page may not have loaded."

        print(f"\nPASS: URL is valid and page loaded successfully.")
        print(f"Current URL : {current_url}")