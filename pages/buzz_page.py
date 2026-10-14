from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BuzzPage(BasePage):
    POST_BOX = (
        By.XPATH,
        '//*[(self::textarea or self::input) and contains(@placeholder, "on your mind")]',
    )
    POST_BTN = (By.XPATH, "//button[normalize-space()='Post']")
    TOAST = (By.CSS_SELECTOR, ".oxd-toast")

    def _post_buttons(self, d):
        return [
            b for b in d.find_elements(*self.POST_BTN)
            if b.is_displayed() and b.is_enabled()
        ]

    def _success(self, message):
        def check(d):
            for t in d.find_elements(*self.TOAST):
                if "Success" in t.text:
                    return True
            posted = d.find_elements(
                By.XPATH, f"//*[contains(normalize-space(text()), '{message}')]"
            )
            return any(p.is_displayed() for p in posted)
        return check

    def create_post(self, message):
        self.wait_loader()
        self.find(self.POST_BOX)
        self.type(self.POST_BOX, message)

        # Pastikan teks benar-benar ada di kotak sebelum menekan Post
        box = self.find(self.POST_BOX)
        isi = box.get_attribute("value") or ""
        assert isi == message, f"Teks tidak masuk ke kotak Post (isi: '{isi}')"

        self.wait.until(lambda d: len(self._post_buttons(d)) > 0)
        btn = self._post_buttons(self.driver)[-1]
        self._highlight(btn)
        self._slow()
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        try:
            self.wait.until(self._success(message))
            return True
        except Exception:
            # Cadangan: muat ulang halaman, lalu cek apakah post sudah muncul
            self.driver.refresh()
            self.wait_loader()
            return self.is_visible(
                (By.XPATH, f"//*[contains(normalize-space(text()), '{message}')]")
            )