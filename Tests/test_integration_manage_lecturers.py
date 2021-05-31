import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

user_username = "user1"
user_password = "userone"
admin_username = "admin"
admin_password = "admin"


class TestManageLecturers:
    def test_manage_lecturers_page(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()
        ff_browser.find_element_by_name("control_panel_link").click()
        ff_browser.find_element_by_id("manageLecturers").click()
        assert "/manage_lecturers" in ff_browser.current_url

    def test_add_remove_lecturer(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()
        ff_browser.find_element_by_name("control_panel_link").click()
        ff_browser.find_element_by_id("manageLecturers").click()

        Select(ff_browser.find_element_by_id("addinstitutions")).select_by_visible_text(
            "A"
        )
        Select(ff_browser.find_element_by_id("addfaculties")).select_by_visible_text(
            "math"
        )
        ff_browser.find_element_by_name("Lecturers Name").send_keys("Dana")
        ff_browser.find_element_by_name("send_add").click()

        Select(
            ff_browser.find_element_by_id("removeinstitutions")
        ).select_by_visible_text("A")
        Select(ff_browser.find_element_by_id("removefaculties")).select_by_visible_text(
            "math"
        )
        Select(ff_browser.find_element_by_id("removelecturers")).select_by_visible_text(
            "Dana"
        )
        ff_browser.find_element_by_name("send_remove").click()
        assert "<p> success" in ff_browser.page_source

    def test_user_cant_manage(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(user_username)
        password.send_keys(user_password)
        btnSubmit.click()
        try:
            ff_browser.find_element_by_name("control_panel_link")
            assert False
        except NoSuchElementException:
            assert True
