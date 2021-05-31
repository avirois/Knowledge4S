from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    session,
    redirect,
)
from modules.selection import Selections
import re
import sqlite3

DB_NAME = "database.db"

manage_lecturers = Blueprint("manage_lecturers", __name__, template_folder="templates")
add_lecturer = Blueprint("add_lecturer", __name__, template_folder="templates")
remove_lecturer = Blueprint("remove_lecturer", __name__, template_folder="templates")


@manage_lecturers.route("/manage_lecturers", methods=["GET"])
@manage_lecturers.route("/manage_lecturers/", methods=["GET"])
@manage_lecturers.route("/manage_lecturers/<status>", methods=["GET"])
def show(status=None):
    if session.get("admin") == None:
        return redirect("/")
    selections = Selections(DB_NAME)
    initial_selections = selections.get_selections()
    return render_template(
        "manage_lecturers.html", **initial_selections, success=status
    )


@add_lecturer.route("/add_lecturer", methods=["POST"])
def add():
    if session.get("admin") == None:
        return redirect("/")
    status: str
    name: str = request.form["Lecturers Name"]
    faculty: str = request.form["faculties"]
    institution: str = request.form["institutions"]
    if checkAddInput(name, institution, faculty):
        add_lecturer_to_db(name, institution, faculty)
        status = "success"
    else:
        status = "fail"
    return redirect(url_for("manage_lecturers.show", status=status))


@remove_lecturer.route("/remove_lecturer", methods=["POST"])
def remove():
    if session.get("admin") == None:
        return redirect("/")
    status: str
    name: str = request.form["lecturers"]
    faculty: str = request.form["faculties"]
    institution: str = request.form["institutions"]
    print(request.form)
    if checkRemoveInput(name, institution, faculty):
        remove_lecturer_from_db(name, institution, faculty)
        status = "success"
    else:
        status = "fail"
    return redirect(url_for("manage_lecturers.show", status=status))


def checkAddInput(lecturername: str, institution: str, faculty: str) -> bool:
    name_re = re.compile(r"([a-zA-Z] *)+")
    if not name_re.fullmatch(lecturername):
        return False
    with sqlite3.connect(DB_NAME) as con:
        cur = con.execute(
            "SELECT InstitutionID FROM Institutions WHERE InstitutionName==?",
            (institution,),
        )
        if len(cur.fetchall()) != 1:
            return False
        cur = con.execute(
            "SELECT FacultyID FROM Faculties WHERE FacultyName==?",
            (faculty,),
        )
        if len(cur.fetchall()) != 1:
            return False
    return True


def checkRemoveInput(name: str, institution: str, faculty) -> bool:
    with sqlite3.connect(DB_NAME) as con:
        facultyID: int
        institutionID: int
        cur = con.execute(
            "SELECT InstitutionID FROM Institutions WHERE InstitutionName==?",
            (institution,),
        )
        institutionsids = cur.fetchall()
        if len(institutionsids) != 1:
            return False
        institutionID = institutionsids[0][0]

        cur = con.execute(
            "SELECT FacultyID FROM Faculties WHERE FacultyName==?",
            (faculty,),
        )
        facultyids = cur.fetchall()
        if len(facultyids) != 1:
            return False
        facultyID = facultyids[0][0]

        cur = con.execute(
            """SELECT LecturerId FROM Lecturers
               WHERE LecturerName==?
                       AND InstitutionID==?
                       AND FacultyID==?
            """,
            (name, institutionID, facultyID),
        )
        if len(cur.fetchall()) != 1:
            return False
    return True


def add_lecturer_to_db(lecturername: str, institution: str, faculty: str) -> None:
    with sqlite3.connect(DB_NAME) as con:
        cur = con.execute(
            "SELECT InstitutionID FROM Institutions WHERE InstitutionName==?",
            (institution,),
        )
        institutionid = cur.fetchone()[0]
        cur = con.execute(
            "SELECT FacultyID FROM Faculties WHERE FacultyName==?",
            (faculty,),
        )
        facultyid = cur.fetchone()[0]
        con.execute(
            """INSERT INTO Lecturers
               (LecturerName,InstitutionID,FacultyID)
               VALUES (?,?,?)""",
            (lecturername, institutionid, facultyid),
        )


def remove_lecturer_from_db(lecturername: str, institution: str, faculty: str) -> None:
    with sqlite3.connect(DB_NAME) as con:
        cur = con.execute(
            "SELECT InstitutionID FROM Institutions WHERE InstitutionName==?",
            (institution,),
        )
        print(institution)
        institutionid = cur.fetchone()[0]
        cur = con.execute(
            "SELECT FacultyID FROM Faculties WHERE FacultyName==?",
            (faculty,),
        )
        facultyid = cur.fetchone()[0]
        cur = con.execute(
            """
            SELECT LecturerID FROM Lecturers
            WHERE LecturerName==?
                AND FacultyID==?
                AND InstitutionID==?
            """,
            (lecturername, facultyid, institutionid),
        )
        lecturerid = cur.fetchone()[0]
        con.execute(
            "DELETE FROM Lecturers WHERE LecturerID == ?",
            (lecturerid,),
        )
