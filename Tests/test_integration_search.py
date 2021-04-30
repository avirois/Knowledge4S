import os
import shutil
from pathlib import Path
import pytest
from selenium import webdriver


def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


@pytest.fixture
def copy_test_storage_1_to_storage():
    os.mkdir("storage")
    shutil.copy("Tests/test_storage_1/1.txt", "storage/1.txt")
    shutil.copy("Tests/test_storage_1/2.txt", "storage/2.txt")
    yield
    rmdir(Path("storage/"))


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
        elm.send_keys("number")

        submit: webdriver.firefox.webdriver.FirefoxWebElement = (
            ff_browser.find_element_by_name("send")
        )
        submit.click()

        res: webdriver.firefox.webdriver.FirefoxWebElement = (
            ff_browser.find_element_by_class_name("fileitem")
        )

        assert "Calculus" in res.text
        assert "study of drawing" in res.text
