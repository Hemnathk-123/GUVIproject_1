import pytest
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


INVALID_CREDENTIALS = [
    ("invalid@email.com", "wrongpassword", "wrong email and password"),
    ("YOUR_EMAIL",        "wrongpassword", "valid email, wrong password"),
    ("",                  "wrongpassword", "empty email"),
    ("invalid@email.com", "",              "empty password"),
]


class TestCase07:

    def setup_method(self):

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self):
        self.driver.quit()

    def _open_signin_page(self):
        self.driver.get("https://www.guvi.in/sign-in/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def _attempt_login(self, email, password):
        # Enter email
        email_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='email' or @name='email' or @id='email']")
        ))
        email_field.clear()
        email_field.send_keys(email)

        # Enter password
        password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.clear()
        password_field.send_keys(password)

        # Login button is <a id="login-btn"> not <button type="submit"> ──
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='login-btn']")
        )).click()

    @pytest.mark.parametrize("email, password, label", INVALID_CREDENTIALS)
    def test_invalid_login(self, email, password, label):
        self._open_signin_page()
        self._attempt_login(email, password)
        print(f"\nAttempted login with: {label}")

        # Wait briefly for page response
        time.sleep(2)
        current_url = self.driver.current_url

        # Assert user stays on sign-in page
        assert "sign-in" in current_url or "guvi.in" in current_url, (
            f"FAIL [{label}]: Unexpected redirect to '{current_url}'"
        )


        try:
            error = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@class,'error') or contains(@class,'alert') or contains(@class,'toast') or contains(@class,'invalid')]")
            ))
            assert error.is_displayed(), f"FAIL [{label}]: Error element found but not visible."
            print(f"PASS [{label}]: Error message displayed — '{error.text}'")
        except Exception:

            assert "sign-in" in self.driver.current_url, (
                f"FAIL [{label}]: No error shown and user was redirected unexpectedly."
            )
            print(f"PASS [{label}]: Login blocked — user remains on sign-in page.")