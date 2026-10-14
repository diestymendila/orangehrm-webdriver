import pytest
from pages.menu_page import MenuPage

# (nama menu, potongan URL yang diharapkan)
MODULES = [
    ("Admin", "admin"),
    ("PIM", "pim"),
    ("Leave", "leave"),
    ("Time", "time"),
    ("Recruitment", "recruitment"),
    ("My Info", "pim/viewPersonalDetails"),
    ("Performance", "performance"),
    ("Dashboard", "dashboard"),
    ("Directory", "directory"),
    ("Maintenance", "maintenance"),
    ("Claim", "claim"),
    ("Buzz", "buzz"),
]


@pytest.mark.parametrize("menu_name,url_part", MODULES, ids=[m[0] for m in MODULES])
def test_open_module(logged_in, menu_name, url_part):
    menu = MenuPage(logged_in)
    menu.open_menu(menu_name)
    menu.url_contains(url_part)
    assert url_part in logged_in.current_url