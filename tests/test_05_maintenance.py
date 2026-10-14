from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import PASSWORD
from pages.base_page import BasePage
from pages.menu_page import MenuPage


def test_maintenance_requires_password(logged_in):
    MenuPage(logged_in).open_menu("Maintenance")
    page = BasePage(logged_in)
    page.type((By.NAME, "password"), PASSWORD)
    page.click((By.CSS_SELECTOR, "button[type='submit']"))
    # Setelah password benar, kolom password hilang dan halaman maintenance terbuka
    page.wait.until(EC.invisibility_of_element_located((By.NAME, "password")))
    assert "maintenance" in logged_in.current_url