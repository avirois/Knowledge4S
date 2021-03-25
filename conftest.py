"""
Global configuration for pytest.

In this file we setup stuff that relate to more than one test.
pytest.fixtures that are session wide setup here.
current fixtures:
    - app_init : starting flask server for all test
    - driver_init :
"""
import os
import threading
from time import sleep
import urllib.request
import urllib.error
import pytest
from selenium import webdriver
from app import app
from sys import platform

# check platform type
# since hosts differ from platform to platform 
if platform != "linux": # FK YOU OLEG REEEEEEEEEEE
    HOST = "127.0.0.1"    
else:
    HOST = "0.0.0.0"

PORT = 5000
TIMEOUT = 5
GECKODRIVER_PATH = os.getenv("GECKODRIVER_PATH")
if not GECKODRIVER_PATH:
    raise RuntimeError("missing GECKODRIVER_PATH variable")


def thread_flask_app():
    """Warper around app.run to be executed in a thread."""
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)


def is_server_running(timeout: float, url: str) -> bool:
    """Try to open url untill timeout."""
    time: float = 0
    while time < timeout:
        try:
            if urllib.request.urlopen(url).getcode() == 200:
                return True
        except urllib.error.URLError:
            pass  # TODO log error
        time += 0.1  # check interval
        sleep(0.1)
    return False


@pytest.fixture(scope="session")
def application():
    """Fixture that start a server in deamon thread."""
    # adding custome logger to read from when server is started
    web_app = threading.Thread(name="Web App", target=thread_flask_app)
    web_app.setDaemon(True)
    web_app.start()
    url = "http://" + HOST + ":" + str(PORT)
    if not is_server_running(TIMEOUT, url):
        raise RuntimeError("time out %d seconds, server not up" % TIMEOUT)
    yield url


@pytest.fixture(scope="session")
def ff_browser():
    """Fixture that starts firefox webdriver headlessly."""
    fire_fox_options = webdriver.FirefoxOptions()
    fire_fox_options.headless = True
    ff_driver = webdriver.Firefox(
        executable_path=GECKODRIVER_PATH, options=fire_fox_options
    )
    yield ff_driver
    ff_driver.close()
