from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PimPage(BasePage):
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    SAVE_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    PERSONAL_HEADER = (By.XPATH, "//h6[normalize-space()='Personal Details']")
    NAME_FILTER = (By.XPATH, "//label[text()='Employee Name']/following::input[1]")
    SEARCH_BTN = (By.XPATH, "//button[normalize-space()='Search']")
    RECORD_INFO = (
        By.XPATH,
        "//span[contains(text(),'Record') and contains(text(),'Found')]",
    )

    def add_employee(self, first, last):
        self.goto("/web/index.php/pim/addEmployee")
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.click(self.SAVE_BTN)
        self.url_contains("viewPersonalDetails")
        self.wait_loader()
        return self.is_visible(self.PERSONAL_HEADER)

    def search_employee(self, last):
        """Cari berdasarkan nama belakang, lalu pastikan barisnya benar-benar ada."""
        self.goto("/web/index.php/pim/viewEmployeeList")
        self.type(self.NAME_FILTER, last)
        self.click(self.SEARCH_BTN)
        self.wait_loader()
        row = (
            By.XPATH,
            f"//div[@class='oxd-table-body']//div[normalize-space()='{last}']",
        )
        return self.is_visible(row)