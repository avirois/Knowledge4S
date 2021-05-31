import pytest
from selenium import webdriver


class TestManageLecturers:
    def test_manage_lecturers_page(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        ff_browser.get(application + "/modification?file_id=1")
        assert "Yosi" in ff_browser.page_source
        assert "F1.txt" in ff_browser.page_source
        assert "2021-01-01" in ff_browser.page_source
