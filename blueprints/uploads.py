from flask import Blueprint, render_template,request,current_app,session
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
    con = sqlite3.connect(current_app.config['DB_NAME'])
    sqlRes = con.execute(sql_query,values)
    rec = sqlRes.fetchall()
    con.commit()
    con.close()

    
def db_update(filename):
    session["username"] = "test"
    now = datetime.now()
    current_date = "{}/{}/{}".format(now.date().day,now.date().month,now.date().year)
    add_query = "INSERT INTO Files (UserName,FileName,Title,Description,DateUpload,DateModified,InstituteID,FacultyID,CourseID) VALUES (?,?,?,?,?,?,?,?,?)"
    values = (  session["username"],#session["username"],# request.form["UserName"],##deoendencies on aviel
                filename,##need generate unic for case two files inside same folder
                request.form["Title"],
                request.form["Description"],
                current_date,
                current_date,
                request.form['InstituteID'],
                request.form['FacultyID'],
                "1",# request.form['CourseID'],##add options for user to pick(check what aviel did)
    )
    print(values)##debug
    add_file_info_to_db(add_query,values)


@upload_blueprint.route("/upload",methods = ['GET', 'POST'])
def upload():
    # Load all institutions
    institutions = []
    con = sqlite3.connect(current_app.config['DB_NAME'])
    # Preprare query
    sqlQueryInstitutions = "SELECT * FROM Institutions"
    # Run the query and save result
    sqlRes = con.execute(sqlQueryInstitutions)
    # Run over the lines of the result and append to list
    for line in sqlRes:
        institutions.append([line[0], line[1]])
    # Close the connection to the database
    con.close()
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            db_update(filename)
            return render_template("upload.html",institutions = institutions,data = { "msg" : "file uploaded successfully"})
        else:
            return render_template("upload.html",institutions = institutions,data = { "msg" : "file type is not supported."})
    else:
        return render_template("upload.html", institutions = institutions, data = {"msg" : ""})
