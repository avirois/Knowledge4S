"""
Global configuration for pytest.

In this file we setup stuff that relate to more than one test.
pytest.fixtures that are session wide setup here.
current fixtures:
    - app_init : starting flask server for all test
    - driver_init :
"""
import os
import logging
from io import StringIO
import threading
from time import sleep
import pytest
from selenium import webdriver
from app import app

HOST = "0.0.0.0"
PORT = 5000
TIMEOUT = 5
GECKODRIVER_PATH = os.getenv("GECKODRIVER_PATH")
if not GECKODRIVER_PATH:
    raise RuntimeError("missing GECKODRIVER_PATH variable")


def thread_flask_app():
    """Warper around app.run to be executed in a thread."""
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)


def is_server_running(timeout, output):
    """If 'Running' been logged than server is running."""
    time = 0
    while time < timeout:
        if "Running" in output.getvalue():
            return True
        time += 0.1  # check interval
        sleep(0.1)
    return False


@pytest.fixture(scope="session")
def app_init():
    """Fixture that start a server in deamon thread."""
    # adding custome logger to read from when server is started
    logger = logging.getLogger("werkzeug")
    output = StringIO()
    handler = logging.StreamHandler(output)
    logger.addHandler(handler)
    web_app = threading.Thread(name="Web App", target=thread_flask_app)
    web_app.setDaemon(True)
    web_app.start()
    if not is_server_running(TIMEOUT, output):
        logger.removeHandler(handler)
        raise RuntimeError("time out %d seconds, server not up")
    logger.removeHandler(handler)
    url = "http://" + HOST + ":" + str(PORT)
    yield url


@pytest.fixture(scope="session")
def driver_init():
    """Fixture that starts firefox webdriver headlessly."""
    fire_fox_options = webdriver.FirefoxOptions()
    fire_fox_options.headless = True
    ff_driver = webdriver.Firefox(
        executable_path=GECKODRIVER_PATH, options=fire_fox_options
    )
    yield ff_driver
    ff_driver.close()
