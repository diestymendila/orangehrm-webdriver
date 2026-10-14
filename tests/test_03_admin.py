from pages.menu_page import MenuPage
from pages.admin_page import AdminPage


def test_admin_search_user(logged_in):
    MenuPage(logged_in).open_menu("Admin")
    assert AdminPage(logged_in).search_user("Admin"), \
        "User 'Admin' tidak ditemukan di tabel hasil pencarian"