import pytest
from selenium import webdriver


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
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("login_link")
        elem.click()
        assert ff_browser.current_url == application + "/login"
    
    def test_register_route(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("register_link")
        elem.click()
        assert ff_browser.current_url == application + "/register"
    
    def test_about_route(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application)
        elem = ff_browser.find_element_by_name("about_link")
        elem.click()
        assert ff_browser.current_url == application + "/about"

