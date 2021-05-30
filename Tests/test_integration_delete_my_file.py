import pytest
import sqlite3
from selenium import webdriver


class TestIntegrationDeleteMyFIle:
    def test_delete_my_file(
        self,
        application: str,
        ff_browser: webdriver.Firefox,
        copy_test_storage_1_to_storage,
        fill_db,
    ):
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys("user1")
        password.send_keys("userone")
        btnSubmit.click()
        ff_browser.get(application + "/delete?id=1")
        with sqlite3.connect("database.db") as con:
            assert (
                len(con.execute("select * from Files where FileID = 1").fetchall()) == 0
            )
