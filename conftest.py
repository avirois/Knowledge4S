"""
Global configuration for pytest.

In this file we setup stuff that relate to more than one test.
pytest.fixtures that are session wide setup here.
current fixtures:
    - app_init : starting flask server for all test
    - driver_init :
    - fill_db()
"""
import os
import threading
from time import sleep
import urllib.request
import urllib.error
import sqlite3
import pytest
from selenium import webdriver
from app import app
from sys import platform

# check platform type
# since hosts differ from platform to platform
if platform != "linux":  # FK YOU OLEG REEEEEEEEEEE
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


DB_NAME = "database.db"


@pytest.fixture
def fill_db():
    with sqlite3.connect(DB_NAME) as con:
        # setup
        con.execute("DELETE FROM Faculties")
        con.execute("DELETE FROM Institutions")
        con.execute("DELETE FROM Lecturers")
        con.execute("DELETE FROM Courses")
        con.execute("DELETE FROM FacIn")
        # 1)
        con.execute("INSERT INTO Institutions VALUES (?, ?)", (1, "A"))
        con.execute("INSERT INTO Faculties VALUES (?, ?)", (11, "math"))

        con.execute("INSERT INTO Lecturers VALUES (?, ?, ?, ?)", (1111, "Moshe", 11, 1))
        con.execute(
            "INSERT INTO Courses VALUES (?, ?, ?, ?)", (111, "Calculus", 1111, 2021)
        )
        con.execute("INSERT INTO FacIn VALUES (?, ?)", (1, 11))
        con.execute(
            "INSERT INTO Files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                1,
                "Yosi",
                "F1.txt",
                "title-math",
                "special number",
                "1.1.2021",
                "1.1.2021",
                1,
                11,
                111,
            ),
        )
        # 2)
        con.execute("INSERT INTO Faculties VALUES (?, ?)", (22, "art"))
        con.execute("INSERT INTO Institutions VALUES (?, ?)", (2, "B"))
        con.execute("INSERT INTO Lecturers VALUES (?, ?, ?, ?)", (2222, "Sarah", 22, 2))
        con.execute(
            "INSERT INTO Courses VALUES (?, ?, ?, ?)",
            (222, "study of drawing", 2222, 2021),
        )
        con.execute("INSERT INTO FacIn VALUES (?, ?)", (2, 22))
        con.execute(
            "INSERT INTO Files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                2,
                "Moshe",
                "F2.txt",
                "titile-sokal",
                "sokal-affair",
                "1.1.2021",
                "1.1.2021",
                2,
                22,
                222,
            ),
        )
    yield
    # Teardown :
    with sqlite3.connect(DB_NAME) as con:
        con.execute("DELETE FROM Faculties")
        con.execute("DELETE FROM Institutions")
        con.execute("DELETE FROM Lecturers")
        con.execute("DELETE FROM Courses")
        con.execute("DELETE FROM FacIn")
        con.execute("DELETE FROM Files")
