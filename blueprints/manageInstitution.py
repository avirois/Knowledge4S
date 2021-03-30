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

@inst_manage_blueprint.route('/manage_institutions', methods=['GET'])
def manage_institutions():

    return render_template('manage_institutions.html', institutions = getInstitutions())
