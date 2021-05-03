import pytest
from selenium import webdriver


class TestSearchIntegration:
    def test_search(
        self,
        application: str,
        ff_browser: webdriver.Firefox,
        copy_test_storage_1_to_storage,
        fill_db,
    ):
        ff_browser.get(application + "/search")

        elm: webdriver.firefox.webdriver.FirefoxWebElement = (
            ff_browser.find_element_by_name("freetextsearch")
        )
        elm.send_keys("sokal")

        submit: webdriver.firefox.webdriver.FirefoxWebElement = (
            ff_browser.find_element_by_name("send")
        )
        submit.click()

        res: list[
            webdriver.firefox.webdriver.FirefoxWebElement
        ] = ff_browser.find_elements_by_class_name("fileitem")

        assert "study of drawing" in res[0].text
