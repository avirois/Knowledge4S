from flask import (
    Blueprint,
    render_template,
    current_app,
    session,
    redirect,
)
import sqlite3

user_files_blueprint = Blueprint(
    "user_files_blueprint", __name__, template_folder="templates"
)


def getFiles():
    dbname = current_app.config["DB_NAME"]
    username = session.get("username")
    with sqlite3.connect(dbname) as con:
        files = []
        cur = con.execute(
            """
        SELECT FileID,FileName,DateUpload,DateModified,Approved
        FROM Files
        WHERE UserName == ?
        """,
            (username,),
        )
        res = cur.fetchall()
        for line in res:
            files.append(
                [
                    line[0],
                    line[1],
                    line[2],
                    line[3],
                    line[4],
                ]
            )
    return files


@user_files_blueprint.route("/user_files", methods=["GET", "POST"])
def user_files_page():
    if session.get("username"):
        return render_template("user_files.html", files=getFiles())
    return redirect("/")
