from flask import Blueprint, render_template,request
from werkzeug.utils import secure_filename
import sqlite3,base64,os,datetime
from datetime import datetime
import os

upload_blueprint = Blueprint("upload_blueprint", __name__, template_folder="templates")
UPLOAD_FOLDER ='storage/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##open connection add info and close
def add_file_info_to_db(sql_query,values):
    with sqlite3.connect(database) as con:
        sqlRes: sqlite3.Cursor = con.execute(sql_query,values)
        return sqlRes.fetchall()

def db_update():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    add_query = "INSERT INTO Files VALUES (?,?,?,?,?,?,?,?,?,?)"
    values = (  
                request.form["UserName"],##deoendencies on aviel
                filename,##need generate unic for case two files inside same folder
                request.form["Title"],##title by user in form
                request.form["Description"],##by user in form
                current_time,
                current_time,
                request.form['InstituteID'],##add options for user to pick
                request.form['FacultyID'],##add options for user to pick(check what aviel did)
                request.form['CourseID'],##add options for user to pick(check what aviel did)
    )
    add_file_info_to_db(add_query,values)


@upload_blueprint.route("/upload",methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            db_update()
            return render_template("upload.html",data = { "msg" : "file uploaded successfully"})
        else:
            return render_template("upload.html",data = { "msg" : "file type is not supported."})
    else:
        return render_template("upload.html", data = {"msg" : ""})
