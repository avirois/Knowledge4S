from flask import Blueprint, render_template, request, session, redirect, current_app, Markup, jsonify
import sqlite3
import os
from static.classes.Institution import Institution

inst_manage_blueprint = Blueprint("manage_institution_blueprint", __name__, template_folder="templates")

def getInstitutions():
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

    return (institutions)

@inst_manage_blueprint.route('/create_institution', methods=['POST', 'GET'])
def create_institution():
    # If method post selected then need to create the institution
    if (request.method == "POST"):
        # connect to db and check if institution already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Get next institution ID
        sqlQueryGetInstID = "SELECT seq FROM sqlite_sequence WHERE name = 'Institutions'"
        sqlResID = con.execute(sqlQueryGetInstID)
        record = sqlResID.fetchone()
        
        # Save the ID of the next institution
        instID = int(record[0]) + 1

        # Get the institution if already exists
        sqlQueryCheckExist = "SELECT * FROM Institutions WHERE InstitutionName = (?)"
        sqlRes = con.execute(sqlQueryCheckExist, (request.form["instName"],))
        record = sqlRes.fetchone()

        # Close the database connection
        con.close()

        # Create institution object
        newInst = Institution(instID, request.form["instName"])
        
        # Check if the institution is not already exists
        if (record == None):
            # connect to DB
            con = sqlite3.connect(current_app.config['DB_NAME'])

            # Insert the institution into institutions table
            sqlQueryCreateInst = "INSERT INTO Institutions (InstitutionName) VALUES (?)"
            con.execute(sqlQueryCreateInst, (newInst.getName(),))

            # Commit the changes in institutions table
            con.commit()

            # Close the database connection
            con.close()
            
            return redirect('/manage_institutions')
        else:
            massage = "Institution already exists"
            return render_template('add_edit_instit.html', operation = "Add new", massage = massage)

    # Load and prepare the page
    else:
        return render_template('add_edit_instit.html', operation = "Add new", massage = "Please enter institution name")


@inst_manage_blueprint.route('/edit_institution/<inst_ID>', methods=['POST', 'GET'])
def edit_institution(inst_ID):

    # If method post selected then need to create the institution
    if (request.method == "POST"):
        # connect to db and check if institution already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Save the ID of the next institution
        instID = int(inst_ID)

        # Create institution object
        newInst = Institution(instID, request.form["instName"])

        # Get the institution data
        sqlQueryGetData = "SELECT * FROM Institutions WHERE InstitutionName = (?)"
        sqlRes = con.execute(sqlQueryGetData, (newInst.getName(),))
        record = sqlRes.fetchone()

        # Check if the institution is not already exists
        if (record == None):
            # connect to DB
            con = sqlite3.connect(current_app.config['DB_NAME'])

            # Update the institution name
            sqlQueryUpdateInst = "UPDATE Institutions SET InstitutionName = (?) WHERE InstitutionID = (?)"
            con.execute(sqlQueryUpdateInst, (newInst.getName(), newInst.getID()))

            # Commit the changes in users table
            con.commit()

            # Close the database connection
            con.close()
            
            return redirect('/manage_institutions')
        else:
            massage = "Institution already exists"
            return render_template('add_edit_instit.html', operation = "Edit", massage = massage, institution = newInst.getName())

        # Close the database connection
        con.close()

    # Load and prepare the page
    else:
        # connect to db and check if institution already exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Save the ID of the next institution
        instID = int(inst_ID)

        # Get the institution data
        sqlQueryGetData = "SELECT * FROM Institutions WHERE InstitutionID = (?)"
        sqlRes = con.execute(sqlQueryGetData, (instID,))
        record = sqlRes.fetchone()

        # Create institution object
        newInst = Institution(instID, record[1])

        return render_template('add_edit_instit.html', operation = "Edit", massage = "Please enter institution name", institution = newInst.getName())

@inst_manage_blueprint.route('/manage_institutions', methods=['GET'])
def manage_institutions():

    return render_template('manage_institutions.html', institutions = getInstitutions())
