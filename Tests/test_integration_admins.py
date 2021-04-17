import pytest
from selenium import webdriver

class TestAdmins:
    def test_admin_info_page(self, application: str, ff_browser: webdriver.Firefox):
        # Open the main page
        ff_browser.get(application)

        # Get admins button
        btnAdmins = ff_browser.find_element_by_name("admins_link")

        # Click the button
        btnAdmins.click()

        # Get header in admins page
        adminsHeader = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (adminsHeader.text == "Information about admins")