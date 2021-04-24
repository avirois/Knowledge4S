import pytest
from selenium import webdriver


class TestAbout:
    def test_about_reachable(self, application: str, ff_browser: webdriver.Firefox):
        ff_browser.get(application + "/about")
        assert "kn0wl463" in ff_browser.page_source
        assert "Our mission" in ff_browser.page_source
