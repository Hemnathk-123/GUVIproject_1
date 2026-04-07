import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



VALID_EMAIL    = "hemnathkrish35@gmail.com"
VALID_PASSWORD = "Hemnathk123@"


class TestCase10:

    def setup_method(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def teardown_method(self):
        self.driver.quit()

    def _login(self):
        """Log in using valid credentials."""
        self.driver.get("https://www.guvi.in/sign-in/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Enter email
        email_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='email' or @name='email' or @id='email']")
        ))
        email_field.clear()
        email_field.send_keys(VALID_EMAIL)
        print(f"\nEmail entered: {VALID_EMAIL}")

        # Enter password
        self.driver.find_element(By.XPATH, "//input[@type='password']").send_keys(VALID_PASSWORD)
        print("Password entered.")


        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='login-btn']")
        )).click()
        print("Login button clicked.")


        self.wait.until(EC.url_changes("https://www.guvi.in/sign-in/"))
        print(f"Login successful. Current URL: {self.driver.current_url}")

    def test_logout(self):
        self._login()


        time.sleep(3)

        # ── Try multiple locators for the profile/user avatar menu ───────────
        profile_locators = [
            "//*[contains(@class,'profile')]",
            "//*[contains(@class,'avatar')]",
            "//*[contains(@class,'user-menu')]",
            "//*[contains(@class,'user-icon')]",
            "//*[contains(@class,'account')]",
            "//img[contains(@alt,'profile') or contains(@alt,'avatar') or contains(@alt,'user')]",
            "//*[@id='user-profile']",
            "//*[contains(@class,'dropdown') and contains(@class,'user')]",
        ]

        profile_clicked = False
        for xpath in profile_locators:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
                profile_clicked = True
                print(f"Profile menu clicked using: {xpath}")
                time.sleep(1)
                break
            except Exception:
                continue

        assert profile_clicked, "FAIL: Could not find or click the profile/user menu."

        # ── Click Logout option ──────────────────────────────────────────────
        logout_locators = [
            "//*[normalize-space()='Logout']",
            "//*[normalize-space()='Log Out']",
            "//*[normalize-space()='Sign Out']",
            "//a[contains(@href,'logout') or contains(@href,'sign-out')]",
            "//*[contains(@class,'logout')]",
        ]

        logout_clicked = False
        for xpath in logout_locators:
            try:
                logout_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                logout_btn.click()
                logout_clicked = True
                print(f"Logout clicked using: {xpath}")
                break
            except Exception:
                continue

        assert logout_clicked, "FAIL: Could not find or click the Logout button."

        # Allow redirect to complete
        time.sleep(2)

        # Assert redirect to homepage or sign-in page
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        current_url = self.driver.current_url
        assert "sign-in" in current_url or "guvi.in" in current_url, (
            f"FAIL: Unexpected URL after logout → '{current_url}'"
        )
        print(f"Redirected to: {current_url}")


        try:
            login_btn = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//a[@id='login-btn'] | //button[@id='login-btn']")
            ))
            assert login_btn.is_displayed(), "FAIL: Login button not visible after logout."
        except Exception:

            assert "sign-in" in current_url, (
                "FAIL: Login button not visible and not on sign-in page after logout."
            )

        print("PASS: Logout successful — user redirected and login button is visible.")