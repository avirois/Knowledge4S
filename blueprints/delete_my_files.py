from flask import Blueprint, request, redirect, current_app, session
import sqlite3

delete_my_file_blueprint = Blueprint(
    "delete_my_file_blueprint", __name__, template_folder="templates"
)


def delete_my_file(dbname, file_id):
    with sqlite3.connect(dbname) as con:
        con.execute("DELETE FROM Files WHERE FileID = ?", (file_id,))
        con.commit()


@delete_my_file_blueprint.route("/delete", methods=["GET"])
def delete():
    if session.get("username"):
        file_id = request.args.get("id")
        if file_id:
            delete_my_file(current_app.config["DB_NAME"], file_id)
        return redirect("/user_files")
    return redirect("/")
