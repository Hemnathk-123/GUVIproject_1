import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



VALID_EMAIL    = "hemnathkrish35@gmail.com"
VALID_PASSWORD = "Hemnathk123@"


class TestCase06:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def test_valid_login(self):
        driver = self.driver

        # Navigate to sign-in page
        driver.get("https://www.guvi.in/sign-in/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("\nNavigated to sign-in page.")

        # Enter email
        email_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='email' or @name='email' or @id='email']")
        ))
        email_field.clear()
        email_field.send_keys(VALID_EMAIL)
        print(f"Email entered: {VALID_EMAIL}")

        # Enter password
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.clear()
        password_field.send_keys(VALID_PASSWORD)
        print("Password entered.")

        # Login button is an <a> tag with id="login-btn" ──────────
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='login-btn']")
        )).click()
        print("Login button clicked.")
        # ────────────────────────────────────────────────────────────────────

        # Assert successful login — URL should change away from sign-in
        self.wait.until(EC.url_changes("https://www.guvi.in/sign-in/"))
        current_url = driver.current_url
        assert "sign-in" not in current_url, (
            f"FAIL: Still on sign-in page after login. URL: '{current_url}'"
        )

        print(f"PASS: Login successful. Redirected to → {current_url}")