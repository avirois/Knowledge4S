import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

user_username = "user1"
user_password = "userone"
admin_username = "admin"
admin_password = "admin"


class TestEditFiles:
    def test_edit_title_of_file_screen(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Perform clean login to the system as admin user
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()

        # Get the view file page
        ff_browser.get(application + "/view?id=2")

        # Find the edit title button and click it
        ff_browser.find_element_by_name("editTitle").click()

        # Get the title of edit title area
        titleEdit = ff_browser.find_element_by_name("titleEditTitle")

        # Get message from login screen
        strMsg = titleEdit.text

        assert (strMsg == "Edit Title")
    
    def test_close_edit_title_screen(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Perform clean login to the system as admin user
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()

        # Get the view file page
        ff_browser.get(application + "/view?id=2")

        # Find the edit title button and click it
        ff_browser.find_element_by_name("editTitle").click()

        # Click on save button
        ff_browser.find_element_by_name("btnClose").click()

        # Get file title
        Title = ff_browser.find_element_by_id("FileTitle").text

        assert (Title == "titile-sokal")
    
    def test_edit_title_of_file(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Set new title for file
        Title = "Test Edit Title"

        # Perform clean login to the system as admin user
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()

        # Get the view file page
        ff_browser.get(application + "/view?id=2")

        # Find the edit title button and click it
        ff_browser.find_element_by_name("editTitle").click()

        # Get the title of edit title area
        editTitleInput = ff_browser.find_element_by_name("title")

        # Clear text area before edit
        editTitleInput.clear()

        # Set new title
        editTitleInput.send_keys("Test Edit Title")

        # Click on save button
        ff_browser.find_element_by_name("btnSaveTitle").click()

        # Get file title
        newTitle = ff_browser.find_element_by_id("FileTitle").text

        assert (newTitle == Title)

