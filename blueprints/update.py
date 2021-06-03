from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    session,
    redirect,
    jsonify,
)
from werkzeug.utils import secure_filename
import sqlite3
import os
import shutil

update_my_file_blueprint = Blueprint(
    "update_my_file_blueprint", __name__, template_folder="templates"
)

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def is_uer_own_file(file_id, username, dbname):
    with sqlite3.connect(dbname) as con:
        cur = con.execute(
            """
            select UserName
            FROM Files
            WHERE FileID == ?
            """,
            (file_id,),
        )
        res = cur.fetchone()
        if res and res[0] == username:
            return True
        return False


def get_filename(file_id, username, dbname):
    with sqlite3.connect(dbname) as con:
        res = con.execute(
            """
            select FileName
            FROM Files
            WHERE FileID == ?
            """,
            (file_id,),
        )
        return res.fetchone()[0]


def backup_current(dbname, file_id):
    with sqlite3.connect(dbname) as con:
        res = con.execute(
            """
            SELECT FileName
            FROM Files
            WHERE FileID == ?
            """,
            (file_id,),
        )
        filename = res.fetchone()[0]
        file_extension = filename.rsplit(".", 1)[1].lower()
        shutil.move(
            os.path.join(
                "storage",
                "{}.{}".format(file_id, file_extension),
            ),
            os.path.join(
                "storage","backup",
                "{}.{}".format(file_id, file_extension),
            ),
        )


def update_file(dbname, file_id, file):
    filename = secure_filename(file.filename)
    with sqlite3.connect(dbname) as con:
        res = con.execute(
            """
            SELECT *
            FROM Files
            WHERE FileID == ?
            """,
            (file_id,),
        )
        row = res.fetchone()
        con.execute(
            """
            DELETE FROM Files
            WHERE FileID == ?
            """,
            (file_id,),
        )
        oldftype = (row[2].split("."))[1]
        oldfilename = str(row[0]) + "." + oldftype
        new_record = row[1:2] + (filename,) + row[3:10] + (0,) + row[11:]
        con.execute(
            """
            INSERT INTO Files
            (UserName, FileName, Title, Description, DateUpload, DateModified, InstituteID, FacultyID, CourseID, Approved, Type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            new_record,
        )
        new_id = con.execute(
            """
            SELECT FileID
            FROM Files
            WHERE
            UserName == ?
            AND FileName == ?
            AND Title == ?
            AND Description == ?
            AND DateUpload == ?
            AND DateModified == ?
            AND InstituteID == ?
            AND FacultyID == ?
            AND CourseID == ?
            AND Approved == ?
            AND Type == ?
            """,
            new_record,
        ).fetchone()[0]
        con.execute(
            """
            DELETE FROM OldFiles
            WHERE FileID == ?
            """,
            (file_id,),
        )
        con.execute(
            """
            INSERT INTO OldFiles
            (FileId,FileName)
            VALUES (?,?)
            """,
            (new_id, oldfilename),
        )
        con.commit()
    newftype = (filename.split("."))[1]
    file.save(os.path.join("storage", str(new_id) + "." + newftype))


def is_supported_filetype(filename):
    return (
        bool(filename)
        and "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@update_my_file_blueprint.route("/update", methods=["GET", "POST"])
def update():
    if not session.get("username"):
        return redirect("/")

    username = session.get("username")
    dbname = current_app.config["DB_NAME"]
    if request.method == "GET":
        file_id = request.args.get("id")
        if not is_uer_own_file(file_id, username, dbname):
            return redirect("/")
        return render_template(
            "update.html",
            msg="",
            file_id=file_id,
            filename=get_filename(file_id, username, dbname),
        )
    else:
        file_id = int(request.form["id"])
        if not is_uer_own_file(file_id, username, dbname):
            return redirect("/")

        file = request.files["file"]

        if not is_supported_filetype(file.filename):
            return render_template(
                "update.html",
                msg="bad file type",
                filename=get_filename(file_id, username, dbname),
            )

        backup_current(dbname, file_id)
        update_file(dbname, file_id, file)

        return render_template("update.html", msg="success", filename=file.filename)
