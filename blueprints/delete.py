from flask import Blueprint, render_template, request, redirect, current_app, session
import sqlite3
from datetime import datetime

delete_blueprint = Blueprint("delete_blueprint", __name__, template_folder="templates")


@delete_blueprint.route("/controlpanel/delete", methods=["POST", "GET"])
def delete():
    try:
        file_id = request.args.get("file_id")
        if file_id is None:
            return redirect("/search")

        con = sqlite3.connect(current_app.config["DB_NAME"])
        user , title = con.execute("SELECT UserName,Title FROM Files WHERE fileID=?",
        (file_id,)).fetchone()
        con.execute("DELETE FROM Files WHERE FileID = ?", (file_id,))
        con.execute("INSERT INTO Notification (User,Date,MSG) VALUES (?,?,?)",
        (
            user,
            datetime.now(),
            "File: " + title + " was removed by an admin",
        ))
        con.commit()
        con.close()
    except Exception as e:
        print(e)
    finally: 
        con.close()
    return redirect("/")
