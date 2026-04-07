import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCase03:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def test_login_button(self):
        driver = self.driver

        # Navigate to GUVI homepage
        driver.get("https://www.guvi.in")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Login button is a <button> tag with id="login-btn" ──────
        login_btn = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='login-btn']")
        ))

        # Assert visibility
        assert login_btn.is_displayed(), "FAIL: Login button is not visible on the homepage."
        print("\nPASS: Login button is visible.")

        # Assert clickability and click
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@id='login-btn']")
        )).click()
        print("Login button clicked.")

        # Assert navigation to login/sign-in page
        self.wait.until(EC.url_contains("sign-in"))
        current_url = driver.current_url
        assert "sign-in" in current_url or "login" in current_url, (
            f"FAIL: Did not navigate to login page. Current URL: '{current_url}'"
        )

        print(f"PASS: Navigated to login page → {current_url}")