import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCase04:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def test_signup_button(self):
        driver = self.driver

        # Navigate to GUVI homepage
        driver.get("https://www.guvi.in")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # ── FIXED: Sign-Up button is a <button> tag with class "secondary-color header-primary-btn" ──
        signup_btn = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[normalize-space()='Sign up' and contains(@class,'header-primary-btn')]")
        ))

        # Assert visibility
        assert signup_btn.is_displayed(), "FAIL: Sign-Up button is not visible on the homepage."
        print("\nPASS: Sign-Up button is visible.")

        # Assert clickability and click
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Sign up' and contains(@class,'header-primary-btn')]")
        )).click()
        print("Sign-Up button clicked.")

        # Assert redirect to register page
        self.wait.until(EC.url_contains("register"))
        current_url = driver.current_url
        assert "register" in current_url, (
            f"FAIL: Did not redirect to register page. Current URL: '{current_url}'"
        )

        print(f"PASS: Sign-Up button redirected to → {current_url}")