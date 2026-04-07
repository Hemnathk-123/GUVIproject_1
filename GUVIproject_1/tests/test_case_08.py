import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCase08:

    def setup_method(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def teardown_method(self):
        self.driver.quit()

    def test_menu_items_visible(self):
        driver = self.driver

        # Navigate to GUVI homepage
        driver.get("https://www.guvi.in")


        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)
        print("\nHomepage loaded.")

        # ─ to match dynamically rendered nav items ──
        menu_items = {
            "Courses": (
                "//*[contains(text(),'Courses') and not(contains(text(),'My Courses'))]"
            ),
            "LIVE Classes": (
                "//*[contains(text(),'LIVE Classes') or contains(text(),'Live Classes') or contains(text(),'LIVE')]"
            ),
            "Practice": (
                "//*[contains(text(),'Practice')]"
            ),
        }

        for item_name, xpath in menu_items.items():
            try:
                # Find all matching elements and check if any is displayed
                elements = driver.find_elements(By.XPATH, xpath)
                visible = any(el.is_displayed() for el in elements if el.text.strip() != "")

                assert visible, f"FAIL: '{item_name}' found in DOM but none are visible."
                print(f"PASS: '{item_name}' is visible in the navigation.")

            except AssertionError:
                print(f"FAIL: '{item_name}' was NOT visible on the page.")
                raise

            except Exception as e:
                print(f"FAIL: '{item_name}' was NOT found on the page. Error: {e}")
                raise AssertionError(f"'{item_name}' menu item not found on homepage.")

        print("\nPASS: All required menu items are visible on the homepage.")