import pytest
from selenium import webdriver

class TestWebStuff:
    def test_title(self, app_init: str, driver_init: webdriver.Firefox):
        url = app_init
        driver_init.get(url)
        assert "hello" == driver_init.title

 
    def test_h1(self, app_init: str, driver_init: webdriver.Firefox):
        url = app_init
        driver_init.get(url)
        tmp = driver_init.find_element_by_tag_name('h1')
        assert "h e ll o" == tmp.text

