import time
from pages.menu_page import MenuPage
from pages.buzz_page import BuzzPage


def test_buzz_create_post(logged_in):
    MenuPage(logged_in).open_menu("Buzz")
    msg = f"Uji Selenium WebDriver {int(time.time())}"
    assert BuzzPage(logged_in).create_post(msg)