import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCase05:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def test_signup_redirect_url(self):
        driver = self.driver

        # Navigate to GUVI homepage
        driver.get("https://www.guvi.in")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Click Sign-Up button
        signup_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Sign up' and contains(@class,'header-primary-btn')]")
        ))
        signup_btn.click()
        print("\nSign-Up button clicked.")

        # Wait for page to load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


        expected_base_url = "https://www.guvi.in/register/"
        current_url = driver.current_url
        assert current_url.startswith(expected_base_url), (
            f"FAIL: URL mismatch.\n"
            f"  Expected to start with : '{expected_base_url}'\n"
            f"  Actual                 : '{current_url}'"
        )
        print(f"PASS: URL matched → {current_url}")

        # Validate page loaded properly
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        assert len(driver.page_source) > 100, "FAIL: Register page did not load properly."
        print("PASS: Register page loaded successfully.")