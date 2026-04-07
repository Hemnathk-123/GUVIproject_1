import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCase02:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def test_page_title(self):
        driver = self.driver

        # Navigate to GUVI homepage
        driver.get("https://www.guvi.in")

        # Wait for title to be present
        self.wait.until(EC.title_contains("GUVI"))

        expected_title = "HCL GUVI | Learn to code in your native language"
        actual_title = driver.title

        assert actual_title == expected_title, (
            f"FAIL: Title mismatch.\n"
            f"  Expected : '{expected_title}'\n"
            f"  Actual   : '{actual_title}'"
        )

        print(f"\nPASS: Page title matches expected value.")
        print(f"Title : {actual_title}")
