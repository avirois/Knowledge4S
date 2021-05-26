from flask import Blueprint, render_template, session, redirect, current_app, request
import sqlite3
from datetime import datetime

controlpanel_blueprint = Blueprint("controlpanel_blueprint", __name__, template_folder="templates")
controlpanel_approve_blueprint = Blueprint("controlpanel_approve_blueprint", __name__, template_folder="templates")
controlpanel_reject_blueprint = Blueprint("controlpanel_reject_blueprint", __name__, template_folder="templates")

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
    return render_template("controlpanel.html",data = data)


@controlpanel_approve_blueprint.route("/controlpanel/approve")
def controlpanel_approve():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')
    file_id = request.args.get("file_id")
    try:
        con = sqlite3.connect(current_app.config['DB_NAME'])
        con.execute("UPDATE Files SET Approved = 1 WHERE FileID = ?",(file_id,))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()
        return redirect("/controlpanel")

@controlpanel_reject_blueprint.route("/controlpanel/reject")
def controlpanel_reject():
    if (session.get("admin") == None):
        return redirect('/')
    file_id = request.args.get("file_id")
    msg  = request.args.get("msg")
    try:
        con = sqlite3.connect(current_app.config['DB_NAME'])
        cur = con.execute("SELECT UserName FROM Files WHERE FileID = ?",(file_id,))
        name = cur.fetchone()[0]
        con.execute("DELETE FROM Files WHERE FileID = ?",(file_id,))
        con.execute("Insert INTO Notification (User,Date,MSG) VALUES (?,?,?)",(
            name,
            datetime.now(),
            msg,
            ))

        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()
        return redirect("/controlpanel")
    return redirect("/controlpanel")