"""
Setup or teardown scenario1.

Copy storage1 to sotorage and setup database acoriding to this scenario:

        * Courses
        CourseID | CourseName         | LecturerID | Year
        ----------------------------------------------------
        |    111 | "Calculus"         | 1111       | 2021 |
        |    222 | "study of drawing" | 2222       | 2021 |

        * FacIn
        InstitutionID | FacultyID
        -------------------------
        |        1    |    11   |
        |        2    |    22   |

        * Faculties
        FacultyID | FacultyName
        ------------------------
        |    11   |     "math" |
        |    22   |     "art"  |

        * Institutions
        InstitutionID | InstitutionName
        --------------------------------
        |          1  |          "A"   |
        |          2  |          "B"   |

        * Lecturers
        LecturerID | LecturerName | FacultyID | InstitutionID |
        -------------------------------------------------------
        |    1111  |      "Moshe" |        11 |          1    |
        |    2222  |      "Sarah" |        22 |          2    |


        * Lecturers
        LecturerID | LecturerName | FacultyID | InstitutionID |
        -------------------------------------------------------
        |    1111  |      "Moshe" |        11 |          1    |
        |    2222  |      "Sarah" |        22 |          2    |

        * Users
        UserName | FirstName | LastName |           Password        |
        -------------------------------------------------------------->>>-
         admin   |  nadmin   |  ladmin  |  encryptPassword(admin)   |
         user1   |  userone  |  ulnone  |  encryptPassword(userone) |
         user2   |  usertwo  |  ulntwo  |  encryptPassword(usertwo) |

         InstitutelID | FacultyID  | StudyYear | Role | IsBanned | Email      |
    ->>>-----------------------------------------------------------------------
         1    |       11   |    2021   |   1  |      0   |  admin@admin.admin |
         1    |       11   |    2021   |   0  |      0   |  user1@user1.user1 |
         2    |       22   |    2021   |   0  |      0   |  user2@user2.user2 |

"""
import os
import shutil
from datetime import date
from pathlib import Path
import sqlite3
from static.classes.User import encryptPassword

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
        con.execute("DELETE FROM Files")
        con.execute("DELETE FROM Files")
        con.execute("DELETE FROM FacIn")
        con.execute("DELETE FROM Users")
        con.execute("DELETE FROM Notification")
        # 1)
        con.execute("INSERT INTO Institutions VALUES (?, ?)", (1, "A"))
        con.execute("INSERT INTO Faculties VALUES (?, ?)", (11, "math"))

        con.execute("INSERT INTO Lecturers VALUES (?, ?, ?, ?)", (1111, "Moshe", 11, 1))
        con.execute(
            "INSERT INTO Courses VALUES (?, ?, ?, ?)", (111, "Calculus", 1111, 2021)
        )
        con.execute("INSERT INTO FacIn VALUES (?, ?)", (1, 11))
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
            "INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "admin",
                "nadmin",
                "ladmin",
                encryptPassword("admin"),
                1,
                11,
                2021,
                1,
                0,
                "admin@admin.admin",
            ),
        )
        con.execute(
            "INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "user1",
                "userone",
                "ulnone",
                encryptPassword("userone"),
                1,
                11,
                2021,
                0,
                0,
                "user1@user1.user1",
            ),
        )
        con.execute(
            "INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "user2",
                "usertwo",
                "ulntwo",
                encryptPassword("usertwo"),
                2,
                22,
                2021,
                0,
                0,
                "user2@user2.user2",
            ),
        )
        con.execute("INSERT INTO Types(Type) VALUES (?) ", ("Lecture",))
        con.execute("INSERT INTO Types(Type) VALUES (?) ", ("Lab",))
        con.execute("INSERT INTO Types(Type) VALUES (?) ", ("Exam",))

    os.mkdir("storage")
    os.mkdir("storage/backup")


def tear_down():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("DELETE FROM Faculties")
        con.execute("DELETE FROM Institutions")
        con.execute("DELETE FROM Lecturers")
        con.execute("DELETE FROM Courses")
        con.execute("DELETE FROM FacIn")
        con.execute("DELETE FROM Files")
        con.execute("DELETE FROM Users")
        con.execute("DELETE FROM Comments")
        con.execute("DELETE FROM Types")
        con.execute("DELETE FROM OldFiles")
        con.execute("DELETE FROM Notification")
        con.execute("DELETE FROM sqlite_sequence")
    rmdir(Path("storage/backup"))
    rmdir(Path("storage/"))


if __name__ == "__main__":
    userinput = input("scenario1:   teardown [0], build [1]:")
    if userinput == "1":
        init()
    if userinput == "0":
        tear_down()
