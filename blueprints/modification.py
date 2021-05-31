import sqlite3
from flask import Blueprint, render_template, request, redirect, current_app, session

database = "database.db"
# /modification?file_id=1

modification_blueprint = Blueprint(
    "modification_blueprint", __name__, template_folder="templates"
)


@modification_blueprint.route("/modification", methods=["GET"])
def view():
    file_id = request.args.get("file_id")
    with sqlite3.connect(database) as con:
        res = con.execute(
            "SELECT UserName, FileName, DateModified FROM Files WHERE FileID==?",
            (file_id,),
        ).fetchone()
        username = res[0]
        file_name = res[1]
        last_modification_date = res[2]
        return render_template(
            "modification.html",
            username=username,
            file_name=file_name,
            last_modification_date=last_modification_date,
        )
