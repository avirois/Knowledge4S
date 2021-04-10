from flask import Blueprint, render_template, request, session, redirect, current_app, Markup, jsonify
import sqlite3
import os
from static.classes.Course import Course

cour_manage_blueprint = Blueprint("manage_course_blueprint", __name__, template_folder="templates")

def getCourses():
    # Load all faculties
    courses = []

    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Preprare query
    sqlQueryCourses = "SELECT * FROM Courses"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryCourses)

    # Run over the lines of the result and append to list
    for line in sqlRes:
        courses.append([line[0], line[1]])

    # Close the connection to the database
    con.close()

    return courses



@cour_manage_blueprint.route('/manage_courses', methods = ['GET', 'POST'])
def manage_courses():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')
    return render_template('manage_courses.html',courses = getCourses())

@cour_manage_blueprint.route('/create_course', methods=['POST', 'GET'])
def create_course():
    # Load all lecturers
    lecturers = []

    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Preprare query
    sqlQueryLecturers = "SELECT * FROM Lecturers"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryLecturers)

    # Run over the lines of the result and append to list
    for line in sqlRes:
        lecturers.append([line[0], line[1]])

    # Close the connection to the database
    con.close()

    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # If method post selected then need to create the course
    if (request.method == "POST"):
        # connect to db and check if course already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Get next course ID
        sqlQueryGetCourID = "SELECT seq FROM sqlite_sequence WHERE name = 'Courses'"
        sqlResID = con.execute(sqlQueryGetCourID)
        record = sqlResID.fetchone()
        
        # Save the ID of the next course
        courID = int(record[0]) + 1

        # Get the course if already exists
        sqlQueryCheckExist = "SELECT * FROM Courses WHERE CourseName = (?)"
        sqlRes = con.execute(sqlQueryCheckExist, (request.form["courName"],))
        record = sqlRes.fetchone()

        # Close the database connection
        con.close()

        # Create course object
        newCour = Course(courID, request.form["courName"],request.form["lecturer"],request.form["year"])

        # Check if not valid course name
        if (not newCour.validateCourse()):
            massage = "Invalid course name or lecturer!"
            return render_template('add_edit_course.html', operation = "Add new", massage = massage,lecturers=lecturers)
        
        # Check if the course is not already exists
        if (record == None):
            
            # connect to DB
            con = sqlite3.connect(current_app.config['DB_NAME'])

            # Insert the course into course table
            sqlQueryCreateCour = "INSERT INTO Courses (CourseName,LecturerID,Year) VALUES (?,?,?)"
            values = (newCour.getName(),newCour.getLact(),newCour.getYear())
            con.execute(sqlQueryCreateCour,values)

            # Commit the changes in faculties table
            con.commit()

            # Close the database connection
            con.close()
            
            return redirect('/manage_courses')
        else:
            massage = "Course already exists"
            return render_template('add_edit_course.html', operation = "Add new", massage = massage,lecturers=lecturers)

    # Load and prepare the page
    else:
        return render_template('add_edit_course.html', operation = "Add new", massage = "Please enter course name",lecturers=lecturers)

@cour_manage_blueprint.route('/edit_course/<cour_ID>', methods=['POST', 'GET'])
def edit_course(cour_ID):
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # If method post selected then need to edit the faculty
    if (request.method == "POST"):
        # connect to db and check if faculty already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Save the ID of the next faculty
        courID = int(cour_ID)

        # Create faculty object
        newCour = Course(courID, request.form["courName"],request.form["lecturer"],request.form["year"])

        # Check if not valid faculty name
        if (not newCour.validateCourse()):
            massage = "Invalid course name or lacturer!"
            return render_template('add_edit_course.html', operation = "Edit", massage = massage, course = newCour.getName())

        # Get the faculty data
        sqlQueryGetData = "SELECT * FROM Courses WHERE CourseName = (?)"
        sqlRes = con.execute(sqlQueryGetData, (newCour.getName(),))
        record = sqlRes.fetchone()

        # Check if the faculty is not already exists
        if (record == None):
            # connect to DB
            con = sqlite3.connect(current_app.config['DB_NAME'])

            # Update the faculty name
            sqlQueryUpdateCour = "UPDATE Courses SET CourseName = (?) WHERE CourseID = (?)"
            con.execute(sqlQueryUpdateCour, (newCour.getName(), newCour.getID()))

            # Commit the changes in faculty table
            con.commit()

            # Close the database connection
            con.close()
            
            return redirect('/manage_courses')
        else:
            massage = "Course already exists"
            return render_template('add_edit_course.html', operation = "Edit", massage = massage, course = newCour.getName())

        # Close the database connection
        con.close()

    # Load and prepare the page
    else:
        # Load all lecturers
        lecturers = []

        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Preprare query
        sqlQueryLecturers = "SELECT * FROM Lecturers"

        # Run the query and save result
        sqlRes = con.execute(sqlQueryLecturers)

        # Run over the lines of the result and append to list
        for line in sqlRes:
            lecturers.append([line[0], line[1]])

        # Close the connection to the database
        con.close()

        # connect to db and check if faculty already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Save the ID of the faculty
        courID = int(cour_ID)

        # Get the faculty data
        sqlQueryGetData = "SELECT * FROM Courses WHERE CourseID = (?)"
        sqlRes = con.execute(sqlQueryGetData, (courID,))
        record = sqlRes.fetchone()

        # Create faculty object
        newCour = Course(courID, record[1],record[2],record[3])

        return render_template('add_edit_course.html', operation = "Edit", massage = "Please enter faculty name", course = newCour.getName(),lect=newCour.getLact(),year=int(newCour.getYear()),lecturers=lecturers)

    