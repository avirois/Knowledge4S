import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
import sqlite3

class TestIntergrationFileUpload:
    def test_file_upload(self, application: str, ff_browser: webdriver.Firefox):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the login page
        ff_browser.get(application + "/login")

        # Get username and password elements on page
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")

        # Get submit button element
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject username and password of test user
        username.send_keys(username_test)
        password.send_keys(password_test)

        # Click on submit button
        btnSubmit.click()

        # Open the create faculty page
        ff_browser.get(application + "/create_faculty")

        # Get faculty name input
        facName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Send value for new faculty
        facName.send_keys(newFacTest)

        # Get save faculty button
        btnSaveFac = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveFac.click()

        # Get title element
        titleSaved = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (titleSaved.text == "Manage Faculties:")