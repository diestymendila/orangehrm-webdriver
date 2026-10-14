import os

BASE_URL = "https://opensource-demo.orangehrmlive.com"
LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
USERNAME = os.getenv("OHRM_USER", "Admin")
PASSWORD = os.getenv("OHRM_PASS", "admin123")
TIMEOUT = 45
LOGIN_TIMEOUT = 90