import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
import sqlite3

# Global variable
# Prepare the user and password for test
username_test = "test111"
password_test = "Aa123456!!"

class TestIntegrationRegister:

    def test_register_page(self, application: str, ff_browser: webdriver.Firefox):
        """Opening main page."""
        ff_browser.get(application)

        # Get the register button element
        btnRegister = ff_browser.find_element_by_xpath("/html/body/div[1]/div[2]/a[4]")

        # Click on login button
        btnRegister.click()

        # Get login screen header
        strRegisterHeader = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        # Get message from login screen
        strMsg = strRegisterHeader.text

        assert (strMsg == "Register")

    def test_register_success(self, application: str, ff_browser: webdriver.Firefox):
        """Opening login page."""
        ff_browser.get(application + "/register")
        
        # Prepare the user and password for test
        #username_test = "test1"
        fname_test = "test1"
        lname_test = "test1"
        #password_test = "Aa123456!"
        institution_test = "SCE"
        faculty_test = "Chemistry"
        year_test = 2

        # Get all elements on register page
        username = ff_browser.find_element_by_name("username")
        fname = ff_browser.find_element_by_name("fName")
        lname = ff_browser.find_element_by_name("lName")
        password = ff_browser.find_element_by_name("password")
        institution = Select(ff_browser.find_element_by_name("institution"))
        faculty = Select(ff_browser.find_element_by_name("faculty"))
        studyYear = ff_browser.find_element_by_name("year")

        # Get submit button element
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject username and password of test user
        username.send_keys(username_test)
        fname.send_keys(fname_test)
        lname.send_keys(lname_test)
        password.send_keys(password_test)
        institution.select_by_visible_text(institution_test)
        sleep(3)
        faculty.select_by_visible_text(faculty_test)
        studyYear.send_keys(year_test)

        # Click on submit button
        btnSubmit.click()

        # Get the welocme message element
        welcomeMsg = ff_browser.find_element_by_xpath("/html/body/div[1]/div[2]/b")

        assert welcomeMsg.text == ("Welcome " + username_test + "!")
        
        # Remove the new created user from DB
