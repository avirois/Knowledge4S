import pytest
import sqlite3
from selenium import webdriver


class TestIntegrationMyReports:
    def test_my_reports(
        self,
        application: str,
        ff_browser: webdriver.Firefox,
        copy_test_storage_1_to_storage,
        fill_db,
    ):
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys("user1")
        password.send_keys("userone")
        btnSubmit.click()
        ff_browser.get(application + "/my_reports")
        assert "My Report" in ff_browser.page_source
