import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

user_username = "user1"
user_password = "userone"
admin_username = "admin"
admin_password = "admin"


class TestForum:
    def test_forum_as_guest(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Perform logout
        ff_browser.get(application + "/logout")

        # Find the forum button and click it
        ff_browser.find_element_by_name("forum_link").click()

        # Get the title of forum
        titleForum = ff_browser.find_element_by_name("forumTitle")

        # Get message from title
        strMsg = titleForum.text

        assert (strMsg == "Forum")

    def test_forum_as_student(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Perform clean login to the system as student user
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(user_username)
        password.send_keys(user_password)
        btnSubmit.click()

        # Find the forum button and click it
        ff_browser.find_element_by_name("forum_link").click()

        # Get the title of forum
        titleForum = ff_browser.find_element_by_name("forumTitle")

        # Get message from title
        strMsg = titleForum.text

        assert (strMsg == "Forum")
    
    def test_forum_as_admin(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Perform clean login to the system as student user
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()

        # Find the forum button and click it
        ff_browser.find_element_by_name("forum_link").click()

        # Get the title of forum
        titleForum = ff_browser.find_element_by_name("forumTitle")

        # Get message from title
        strMsg = titleForum.text

        assert (strMsg == "Forum")
    
    def test_forum_of_course(
        self, application: str, ff_browser: webdriver.Firefox, fill_db
    ):
        # Perform clean login to the system as student user
        ff_browser.get(application + "/logout")
        ff_browser.get(application + "/login")
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")
        username.send_keys(admin_username)
        password.send_keys(admin_password)
        btnSubmit.click()

        # Find the forum button and click it
        ff_browser.find_element_by_name("forum_link").click()

        # Click on selected institution button
        ff_browser.find_element_by_name("btnInstA").click()

        # Click on selected faculty button
        ff_browser.find_element_by_name("btnFacmath").click()

        # Click on selected course button
        ff_browser.find_element_by_name("btnCourseCalculus").click()

        # Get the title of forum
        titleForum = ff_browser.find_element_by_name("courseForumTitle")

        # Get message from title
        strMsg = titleForum.text

        assert (strMsg == "forum of Calculus")