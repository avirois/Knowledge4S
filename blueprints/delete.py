from flask import Blueprint, render_template, request, redirect , current_app, session
import sqlite3
from datetime import datetime

delete_blueprint = Blueprint("delete_blueprint", __name__, template_folder="templates")

@delete_blueprint.route("/controlpanel/delete",methods = ['POST','GET'])
def delete():
    file_id = request.args.get("file_id")
    if file_id is None:
        return redirect('/search')

    con = sqlite3.connect(current_app.config["DB_NAME"])
    con.execute("DELETE FROM Files WHERE FileID = ?",(file_id,))
    con.commit()
    con.close()
    return redirect('/')

