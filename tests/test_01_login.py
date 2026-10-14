from config import USERNAME, PASSWORD
from pages.login_page import LoginPage
from pages.menu_page import MenuPage


def test_login_valid_credentials(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    menu = MenuPage(driver)
    assert menu.dashboard_loaded()
    assert driver.title == "OrangeHRM"


def test_login_invalid_password(driver):
    page = LoginPage(driver).open()
    page.login(USERNAME, "salah123")
    assert "Invalid credentials" in page.error_text()


def test_logout_functionality(logged_in):
    MenuPage(logged_in).logout()
    LoginPage(logged_in).url_contains("auth/login")
    assert "auth/login" in logged_in.current_url