from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class AdminPage(BasePage):
    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/following::input[1]")
    SEARCH_BTN = (By.XPATH, "//button[normalize-space()='Search']")

    @staticmethod
    def _row(username):
        return (
            By.XPATH,
            f"//div[@class='oxd-table-body']//div[normalize-space()='{username}']",
        )

    def search_user(self, username):
        """Cari user, lalu pastikan barisnya benar-benar muncul di tabel hasil."""
        self.url_contains("admin/viewSystemUsers")
        for attempt in range(2):  # kalau klik pertama tidak memicu hasil, ulangi sekali
            self.type(self.USERNAME_INPUT, username)
            self.click(self.SEARCH_BTN)
            self.wait_loader()
            try:
                WebDriverWait(self.driver, 25).until(
                    EC.visibility_of_element_located(self._row(username))
                )
                return True
            except TimeoutException:
                continue
        return False