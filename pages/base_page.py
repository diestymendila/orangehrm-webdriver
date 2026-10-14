import os
import time
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import TIMEOUT, BASE_URL

# Untuk keperluan video: SLOW_MO=1 memberi jeda 1 detik setelah tiap aksi
SLOW_MO = float(os.getenv("SLOW_MO", "0"))

# Overlay loading milik OrangeHRM yang sering menghalangi klik
LOADER = (By.CSS_SELECTOR, ".oxd-form-loader, .oxd-loading-spinner")


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def _slow(self):
        if SLOW_MO:
            time.sleep(SLOW_MO)

    def _highlight(self, element):
        try:
            self.driver.execute_script(
                "arguments[0].style.outline='3px solid red';", element
            )
        except Exception:
            pass

    def wait_loader(self):
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.invisibility_of_element_located(LOADER)
            )
        except TimeoutException:
            pass

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        last_error = None
        for attempt in range(3):
            try:
                self.wait_loader()
                el = self.wait.until(EC.element_to_be_clickable(locator))
                self._highlight(el)
                self._slow()
                try:
                    el.click()
                except ElementClickInterceptedException:
                    self.wait_loader()
                    self.driver.execute_script("arguments[0].click();", el)
                return
            except StaleElementReferenceException as e:
                last_error = e
                time.sleep(1)
        raise last_error

    def set_value(self, el, text):
        """Isi kolom lewat JavaScript dan kirim event agar Vue/OrangeHRM membacanya."""
        self.driver.execute_script(
            """
            const el = arguments[0], val = arguments[1];
            const proto = el.tagName === 'TEXTAREA'
                ? window.HTMLTextAreaElement.prototype
                : window.HTMLInputElement.prototype;
            Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            """,
            el,
            text,
        )

    def type(self, locator, text):
        last_error = None
        for attempt in range(3):
            try:
                self.wait_loader()
                el = self.find(locator)
                self._highlight(el)
                try:
                    el.click()
                except ElementClickInterceptedException:
                    self.wait_loader()
                    self.driver.execute_script("arguments[0].focus();", el)
                el.send_keys(Keys.CONTROL, "a", Keys.NULL)
                el.send_keys(Keys.DELETE)
                el.send_keys(text)
                if (el.get_attribute("value") or "") != text:
                    self.set_value(el, text)
                self._slow()
                return
            except StaleElementReferenceException as e:
                last_error = e
                time.sleep(1)
        raise last_error

    def text_of(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            self.find(locator)
            return True
        except Exception:
            return False

    def url_contains(self, fragment):
        return self.wait.until(EC.url_contains(fragment))

    def goto(self, path):
        """Buka halaman langsung lewat URL (lebih stabil daripada klik menu)."""
        self.driver.get(f"{BASE_URL}{path}")
        self.wait_loader()