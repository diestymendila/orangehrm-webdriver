import os
import socket
import time
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import USERNAME, PASSWORD, LOGIN_TIMEOUT
from pages.login_page import LoginPage


@pytest.fixture(scope="session", autouse=True)
def cek_koneksi():
    """Berhenti cepat dengan pesan jelas kalau situs demo tidak bisa dijangkau."""
    host = "opensource-demo.orangehrmlive.com"
    try:
        socket.create_connection((host, 443), timeout=10).close()
    except OSError:
        pytest.exit(
            f"Tidak bisa terhubung ke {host}. Cek internet/DNS lalu jalankan ulang.",
            returncode=2,
        )


def _create_driver():
    last_error = None
    for attempt in range(3):  # peluncuran Firefox pertama kali kadang gagal
        try:
            opts = Options()
            # "eager": tidak menunggu semua gambar/aset selesai dimuat
            opts.page_load_strategy = "eager"
            headless = os.getenv("HEADLESS") == "1"
            if headless:
                opts.add_argument("-headless")

            grid_url = os.getenv("GRID_URL")  # contoh: http://localhost:4444
            if grid_url:
                driver = webdriver.Remote(command_executor=grid_url, options=opts)
            else:
                driver = webdriver.Firefox(options=opts)

            driver.set_page_load_timeout(90)

            if headless:
                driver.set_window_size(1366, 768)
            else:
                driver.maximize_window()
            return driver
        except WebDriverException as e:
            last_error = e
            time.sleep(3)
    raise last_error


@pytest.fixture
def driver():
    d = _create_driver()
    yield d
    try:
        d.quit()
    except Exception:
        pass


@pytest.fixture
def logged_in(driver):
    login = LoginPage(driver)
    dashboard_h6 = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    last_error = None
    for attempt in range(3):  # login diulang di dalam fixture (bukan rerun test)
        try:
            login.open().login(USERNAME, PASSWORD)
            WebDriverWait(driver, LOGIN_TIMEOUT).until(EC.url_contains("dashboard"))
            WebDriverWait(driver, LOGIN_TIMEOUT).until(
                EC.visibility_of_element_located(dashboard_h6)
            )
            return driver
        except WebDriverException as e:
            last_error = e
            time.sleep(3)
    pytest.fail(f"Login gagal setelah 3 percobaan: {type(last_error).__name__}")


# ---- Reporting: screenshot otomatis di setiap test (pass maupun fail) ----
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return
    try:
        import pytest_html
        png = drv.get_screenshot_as_base64()
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(png, name="Screenshot"))
        report.extras = extras
    except Exception:
        pass