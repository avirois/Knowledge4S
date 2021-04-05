from flask import Blueprint, render_template,request,current_app,session, redirect,jsonify
from werkzeug.utils import secure_filename
import sqlite3,base64,os,datetime
from datetime import datetime
from modules.search import SearchEngine
import os

upload_blueprint = Blueprint("upload_blueprint", __name__, template_folder="templates")
UPLOAD_FOLDER ='storage/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    return sqlRes.lastrowid

def db_update(filename,file):
    now = datetime.now()
    current_date = "{}/{}/{}".format(now.date().day,now.date().month,now.date().year)
    add_query = "INSERT INTO Files (UserName,FileName,Title,Description,DateUpload,DateModified,InstituteID,FacultyID,CourseID) VALUES (?,?,?,?,?,?,?,?,?)"
    values = (  session["username"],
                filename,
                request.form["Title"],
                request.form["Description"],
                now,
                now,
                request.form['InstituteID'],
                request.form['FacultyID'],
                request.form['CourseID'],
    )
    file_id = add_file_info_to_db(add_query,values)
    file_extension = filename.rsplit('.', 1)[1].lower()
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "{}.{}".format(file_id,file_extension)))
    SearchEngine(None).add_document(file_id, request.form["Description"], filename, request.form["Title"])
    

@upload_blueprint.route("/upload",methods = ['GET', 'POST'])
def upload():
    if (session.get('username') == None):
        return redirect('/')
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
            db_update(filename,file)
            return render_template("upload.html",institutions = institutions,data = { "msg" : "file uploaded successfully"})
        else:
            return render_template("upload.html",institutions = institutions,data = { "msg" : "file type is not supported."})
    else:
        return render_template("upload.html", institutions = institutions, data = {"msg" : ""})

@upload_blueprint.route('/upload/course/<facul_ID>')
def courseByfaculty(facul_ID):
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Create list of courses in current faculties
    coursInfac = []

    # Preprare query
    sqlQueryCourses = "SELECT CourseID,CourseName FROM Courses WHERE LecturerID IN (SELECT LecturerID from Lecturers WHERE FacultyID = (?))"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryCourses, (int(facul_ID),))

    # Run over the lines of the result and append to list
    for line in sqlRes:
        course = {}
        course['courID'] = line[0]
        course['courName'] = line[1]
        coursInfac.append(course)

    # Close the connection to the database
    con.close()

    # Create json from the result list
    return jsonify({'courInst' : coursInfac})
