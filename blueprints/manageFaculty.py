from flask import Blueprint, render_template, request, session, redirect, current_app, Markup, jsonify
import sqlite3
import os
from static.classes.Faculty import Faculty

fac_manage_blueprint = Blueprint("manage_faculty_blueprint", __name__, template_folder="templates")

def getFaculties():
    # Load all faculties
    faculties = []

    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Preprare query
    sqlQueryFaculties = "SELECT * FROM Faculties"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryFaculties)

    # Run over the lines of the result and append to list
    for line in sqlRes:
        faculties.append([line[0], line[1]])

    # Close the connection to the database
    con.close()

    return (faculties)


@fac_manage_blueprint.route('/create_faculty', methods=['POST', 'GET'])
def create_faculty():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # If method post selected then need to create the faculty
    if (request.method == "POST"):
        # connect to db and check if faculty already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Get next faculty ID
        sqlQueryGetFacID = "SELECT seq FROM sqlite_sequence WHERE name = 'Faculties'"
        sqlResID = con.execute(sqlQueryGetFacID)
        record = sqlResID.fetchone()
        
        # Save the ID of the next faculty
        facID = int(record[0]) + 1

        # Get the faculty if already exists
        sqlQueryCheckExist = "SELECT * FROM Faculties WHERE FacultyName = (?)"
        sqlRes = con.execute(sqlQueryCheckExist, (request.form["facName"],))
        record = sqlRes.fetchone()

        # Close the database connection
        con.close()

        # Create faculty object
        newFac = Faculty(facID, request.form["facName"])

        # Check if not valid faculty name
        if (not newFac.validateFaculty()):
            massage = "Invalid faculty name!"
            return render_template('add_edit_faculty.html', operation = "Add new", massage = massage)
        
        # Check if the faculty is not already exists
        if (record == None):
            # connect to DB
            con = sqlite3.connect(current_app.config['DB_NAME'])

            # Insert the faculty into faculty table
            sqlQueryCreateFac = "INSERT INTO Faculties (FacultyName) VALUES (?)"
            con.execute(sqlQueryCreateFac, (newFac.getName(),))

            # Commit the changes in faculties table
            con.commit()

            # Close the database connection
            con.close()
            
            return redirect('/manage_faculties')
        else:
            massage = "Faculty already exists"
            return render_template('add_edit_faculty.html', operation = "Add new", massage = massage)

    # Load and prepare the page
    else:
        return render_template('add_edit_faculty.html', operation = "Add new", massage = "Please enter faculty name")


@fac_manage_blueprint.route('/edit_faculty/<fac_ID>', methods=['POST', 'GET'])
def edit_faculty(fac_ID):
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # If method post selected then need to edit the faculty
    if (request.method == "POST"):
        # connect to db and check if faculty already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Save the ID of the next faculty
        facID = int(fac_ID)

        # Create faculty object
        newFac = Faculty(facID, request.form["facName"])

        # Check if not valid faculty name
        if (not newFac.validateFaculty()):
            massage = "Invalid faculty name!"
            return render_template('add_edit_faculty.html', operation = "Edit", massage = massage, faculty = newFac.getName())

        # Get the faculty data
        sqlQueryGetData = "SELECT * FROM Faculties WHERE FacultyName = (?)"
        sqlRes = con.execute(sqlQueryGetData, (newFac.getName(),))
        record = sqlRes.fetchone()

        # Check if the faculty is not already exists
        if (record == None):
            # connect to DB
            con = sqlite3.connect(current_app.config['DB_NAME'])

            # Update the faculty name
            sqlQueryUpdateFac = "UPDATE Faculties SET FacultyName = (?) WHERE FacultyID = (?)"
            con.execute(sqlQueryUpdateFac, (newFac.getName(), newFac.getID()))

            # Commit the changes in faculty table
            con.commit()

            # Close the database connection
            con.close()
            
            return redirect('/manage_faculties')
        else:
            massage = "Faculty already exists"
            return render_template('add_edit_faculty.html', operation = "Edit", massage = massage, faculty = newFac.getName())

        # Close the database connection
        con.close()

    # Load and prepare the page
    else:

        # connect to db and check if faculty already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Save the ID of the faculty
        facID = int(fac_ID)

        # Get the faculty data
        sqlQueryGetData = "SELECT * FROM Faculties WHERE FacultyID = (?)"
        sqlRes = con.execute(sqlQueryGetData, (facID,))
        record = sqlRes.fetchone()

        # Create faculty object
        newFac = Faculty(facID, record[1])

        return render_template('add_edit_faculty.html', operation = "Edit", massage = "Please enter faculty name", faculty = newFac.getName())

@fac_manage_blueprint.route('/manage_faculties', methods=['GET'])
def manage_faculties():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    return render_template('manage_faculties.html', faculties = getFaculties())