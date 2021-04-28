from flask import Blueprint, render_template, session, redirect, current_app
import sqlite3

controlpanel_blueprint = Blueprint("controlpanel_blueprint", __name__, template_folder="templates")


@controlpanel_blueprint.route("/controlpanel")
def controlpanel():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # get all the preapproved files and display them
    data = []
    try:
        con = sqlite3.connect(current_app.config['DB_NAME'])
        cur = con.execute("SELECT FileID,UserName,Title,Description,DateUpload," +
        "Institutions.InstitutionName,Faculties.FacultyName,Courses.CourseName " +
        "FROM Files " + 
        "NATURAL JOIN Institutions,Faculties,Courses " + 
        "WHERE Approved = 0 " + 
        "AND Files.InstituteID = Institutions.InstitutionID " + 
        "AND Files.FacultyID = Faculties.FacultyID " + 
        "AND Files.CourseID = Courses.CourseID " )
        for row in cur:
            data.append(row)
    except Exception as e:
        print(e)
    finally:
        con.close()
    print(data)
    return render_template("controlpanel.html",data = data)
