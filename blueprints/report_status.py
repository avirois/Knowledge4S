import sqlite3
from flask import Blueprint, render_template, request, redirect, current_app, session

database = "database.db"

my_reports_blueprint = Blueprint(
    "my_reports_blueprint", __name__, template_folder="templates"
)

def parse_file_time(string):
    tmp = string.split(" ")
    date = tmp[0]
    time = tmp[1]
    date = date.split("-")
    time = time.split(":")
    return "{}/{}/{} - {}:{}".format(date[2],date[1],date[0],time[0],time[1])

def get_my_report(dbname, username):
    with sqlite3.connect(dbname) as con:
        res = con.execute(
            """
            SELECT Date,Reason
            FROM Reports
            WHERE Reporter == ?
            """,
            (username,),
        ).fetchall()
        return list(map(lambda t: {"date": parse_file_time(t[0]), "reason": t[1]}, res))


@my_reports_blueprint.route("/my_reports", methods=["GET"])
def view():
    if not session.get("username"):
        return redirect("/")
    username = session.get("username")
    return render_template("my_reports.html", reports=get_my_report(database, username))
