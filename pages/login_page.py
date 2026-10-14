from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import LOGIN_URL


class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    def open(self):
        self.driver.get(LOGIN_URL)
        self.find(self.USERNAME)
        return self

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def error_text(self):
        return self.text_of(self.ERROR_MSG)