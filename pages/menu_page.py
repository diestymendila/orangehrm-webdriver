from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MenuPage(BasePage):
    HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT = (By.XPATH, "//a[normalize-space()='Logout']")

    @staticmethod
    def _menu(name):
        return (
            By.XPATH,
            f"//a[contains(@class,'oxd-main-menu-item')]"
            f"//span[normalize-space()='{name}']",
        )

    def dashboard_loaded(self):
        return self.is_visible(self.HEADER)

    def open_menu(self, name):
        self.click(self._menu(name))

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT)