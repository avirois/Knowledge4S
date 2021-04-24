import os
import shutil
from pathlib import Path
import sqlite3

DB_NAME = "database.db"
TEST_STORAGE_1 = "Tests/test_storage_1"


def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


def init():
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

    os.mkdir("storage")
    shutil.copy("Tests/test_storage_1/1.txt", "storage/1.txt")
    shutil.copy("Tests/test_storage_1/2.txt", "storage/2.txt")


def tear_down():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("DELETE FROM Faculties")
        con.execute("DELETE FROM Institutions")
        con.execute("DELETE FROM Lecturers")
        con.execute("DELETE FROM Courses")
        con.execute("DELETE FROM FacIn")
        con.execute("DELETE FROM Files")
    rmdir(Path("storage/"))


if __name__ == "__main__":
    userinput = input("scenario1:   teardown [0], build [1]:")
    if userinput == "1":
        init()
    if userinput == "0":
        tear_down()
