import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCase09:

    def setup_method(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def teardown_method(self):
        self.driver.quit()

    def test_dobby_assistant_present(self):
        driver = self.driver

        # Navigate to GUVI homepage
        driver.get("https://www.guvi.in")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


        time.sleep(6)
        print("\nHomepage loaded. Searching for Dobby Assistant (Zoho SalesIQ)...")

        dobby_found = False

        # ── Strategy 1: Locate using the exact element from the page ─────────
        # <span class="siqico-close zsiq-close-icn" id="zs_fl_close">
        zoho_locators = [
            (By.ID,    "zs_fl_close"),
            (By.XPATH, "//*[@id='zs_fl_close']"),
            (By.XPATH, "//*[contains(@class,'zsiq-close-icn')]"),
            (By.XPATH, "//*[contains(@class,'siqico-close')]"),
            (By.XPATH, "//*[contains(@aria-label,'live chat')]"),
            (By.XPATH, "//*[contains(@aria-label,'Minimize live chat')]"),
        ]

        for by, locator in zoho_locators:
            try:
                element = driver.find_element(by, locator)
                if element:
                    dobby_found = True
                    print(f"PASS: Dobby Assistant found in main DOM → {locator}")
                    break
            except Exception:
                continue

        # ── Strategy 2: Search inside Zoho SalesIQ iframes ──────────────────
        if not dobby_found:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            print(f"Checking {len(iframes)} iframe(s) for Zoho SalesIQ widget...")
            for i, iframe in enumerate(iframes):
                try:
                    src   = iframe.get_attribute("src") or ""
                    title = iframe.get_attribute("title") or ""
                    name  = iframe.get_attribute("name") or ""
                    combined = (src + title + name).lower()
                    print(f"  iframe[{i}]: src={src[:60]} | title={title}")
                    if any(kw in combined for kw in ["zsiq", "zoho", "salesiq", "chat", "dobby", "zs_"]):
                        dobby_found = True
                        print(f"PASS: Zoho SalesIQ iframe found → {src}")
                        break

                    # Switch into iframe and look for Zoho elements inside
                    driver.switch_to.frame(iframe)
                    inner_elements = driver.find_elements(
                        By.XPATH, "//*[contains(@class,'zsiq') or contains(@id,'zs_')]"
                    )
                    if inner_elements:
                        dobby_found = True
                        print(f"PASS: Zoho SalesIQ element found inside iframe[{i}]")
                        driver.switch_to.default_content()
                        break
                    driver.switch_to.default_content()

                except Exception:
                    driver.switch_to.default_content()
                    continue

        # ── Strategy 3: Scan page source for Zoho SalesIQ keywords ──────────
        if not dobby_found:
            page_source = driver.page_source.lower()
            keywords = ["zsiq", "zoho", "salesiq", "zs_fl_close", "siqico", "dobby"]
            for kw in keywords:
                if kw in page_source:
                    dobby_found = True
                    print(f"PASS: Zoho SalesIQ keyword '{kw}' found in page source.")
                    break

        # ── Final assertion ──────────────────────────────────────────────────
        assert dobby_found, (
            "FAIL: Dobby GUVI Assistant (Zoho SalesIQ) was not found in DOM, "
            "iframes, or page source. The widget may not have loaded in time."
        )

        print("PASS: Dobby GUVI Assistant is present on the homepage.")