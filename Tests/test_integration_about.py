import pytest
from selenium import webdriver


class TestAbout:
    def test_about_reachable(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/about")
        assert "kn0wl463" in ff_browser.page_source
        assert "Our mission" in ff_browser.page_source

    def test_about_githublink(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/about")

        link: webdriver.firefox.webdriver.FirefoxWebElement = (
            ff_browser.find_element_by_id("link")
        )
        link.click()
        assert ff_browser.current_url == "https://github.com/avirois/Knowledge4S"
