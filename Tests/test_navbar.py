import pytest
from selenium import webdriver
from flask import current_app
import sqlite3

#globals
t_username = 'testUsername29475'
t_password = 'kjdfvi4kjvsd4'
t_firstname = 'john'
t_lastname =  'doe'
DB_NAME = 'database.db'

def clean_DB():
    connection = sqlite3.connect(DB_NAME)
    cur = connection.execute("DELETE FROM Users WHERE UserName=(?)",(t_username,))
    connection.commit()
    connection.close()


class TestNavbar:
    
    # ---------------------------------
    # navbar gui tests
    # ---------------------------------

    # guest gui testing 
    def test_navbar_home_link(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("home_link")
        assert elem.text == "Home"
    
    def test_navbar_login_link(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/logout")
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("login_link")
        assert elem.text == "Login"

    def test_navbar_register_link(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/logout")
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("register_link")
        assert elem.text == "Register"
    
    def test_navbar_about_link(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("about_link")
        assert elem.text == "About"
        

    # ---------------------------------
    # navbar unitests
    # ---------------------------------

    def test_home_route(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("home_link")
        elem.click()
        assert ff_browser.current_url == application + "/"

    def test_login_route(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/logout")
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("login_link")
        elem.click()
        assert ff_browser.current_url == application + "/login"
    
    def test_register_route(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/logout")
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("register_link")
        elem.click()
        assert ff_browser.current_url == application + "/register"
    '''
    # uncomment next sprint
    def test_about_route(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("about_link")
        elem.click()
        assert ff_browser.current_url == application + "/about"
    '''
    #remove previous inserts
    clean_DB()

    def test_user_navbar(self, application: str, ff_browser: webdriver.Firefox):
        connection = sqlite3.connect(DB_NAME)

        #insert normal user
        cur = connection.execute("INSERT INTO Users VALUES (?,?,?,?,?,?,?,?,?)",
            (t_username,t_firstname,t_lastname,t_password,1,1,1,0,0,)
        )

        connection.commit()
        connection.close()

        #connect to user
        ff_browser.get(application + "/login")
        elem = ff_browser.find_element_by_name("username")
        elem.send_keys(t_username)
        elem = ff_browser.find_element_by_name("password")
        elem.send_keys(t_password)
        elem = ff_browser.find_element_by_name("submit")
        elem.click()
        elem = ff_browser.find_element_by_name("user_link")
        assert elem.text == "My Profile"

    #remove previous inserts
    clean_DB()