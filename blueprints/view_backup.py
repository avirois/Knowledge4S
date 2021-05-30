from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
)
import sqlite3

view_backup_blueprint = Blueprint(
    "view_backup_blueprint", __name__, template_folder="templates"
)


@view_backup_blueprint.route("/view_backup", methods=["GET"])
def show():
    dbname = current_app.config["DB_NAME"]
    file_id = request.args.get("id")

    exist = False
    filename = None
    with sqlite3.connect(dbname) as con:
        cur = con.execute(
            """
            select FileName
            FROM OldFiles
            WHERE FileID == ?
            """,
            (file_id,),
        )
        res = cur.fetchone()
        if res and len(res) == 1:
            filename = res[0]
            exist = True

    return render_template(
        "view_backup.html", exist=exist, file_id=file_id, filename=filename
    )
