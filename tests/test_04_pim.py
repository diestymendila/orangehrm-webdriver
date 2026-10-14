import time
from pages.pim_page import PimPage


def test_pim_add_and_search_employee(logged_in):
    last = f"Uji{int(time.time())}"
    pim = PimPage(logged_in)
    assert pim.add_employee("Budi", last), "Employee gagal disimpan"
    assert pim.search_employee(last), "Employee baru tidak ditemukan di daftar"