import pytest
from selenium import webdriver


class TestWebStuff:
    """Two example tests that require the use of application and browser."""

    def test_title(self, application: str, ff_browser: webdriver.Firefox):
        """Opening main page and checking the title."""
        ff_browser.get(application)
        assert ff_browser.title == "hello"

    def test_h1(self, application: str, ff_browser: webdriver.Firefox):
        """Opening main page and checking the first h1."""
        ff_browser.get(application)
        # in code comlition not working well you can add type hinting for
        # elements
        elm: webdriver.firefox.webdriver.FirefoxWebElement = (
            ff_browser.find_element_by_tag_name("h1")
        )
        assert elm.text == "h e ll o"
