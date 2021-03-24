from flask import Blueprint, render_template, request, session, redirect, current_app, Markup
import sqlite3
import os
from static.classes.User import User

authentication_blueprint = Blueprint("authentication_blueprint", __name__, template_folder="templates")

@authentication_blueprint.route('/login',methods=['POST','GET'])
def login():
    # Check if user already logged in
    if ('username' in session):
        return redirect('/')
    # Check if post method selected therfore need to login the user
    if request.method == "POST":
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])
        sqlQuryLogin = "SELECT UserName, Password, Role FROM Users WHERE username = (?)"
        sqlRes = con.execute(sqlQuryLogin,(request.form["username"],))
        record = sqlRes.fetchone()

        # Check if the user exists
        if ((record != None) and (request.form["password"] == record[1])):
            # Check if the user is admin or not
            if record[2] == 1:
                session['admin'] = True
                
            session['username'] = request.form["username"]
            massage = "Logged in successfuly!"
            return redirect('/')
        # The password is incorrect
        else:
            massage = "Wrong password entered!"

        # Close the connection to DB
        con.close()

        return render_template('login.html', massage = massage)
    # Get method mean open the page
    else:
        return render_template('login.html', massage = "Please fill the login form!")

@authentication_blueprint.route('/register',methods=['POST','GET'])
def register():
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Load all institutions
    institutions = []

    # Preprare query
    sqlQueryInstitutions = "SELECT * FROM Institutions"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryInstitutions)

    # Run over the lines of the result and append to list
    for line in sqlRes:
        institutions.append([line[0], line[1]])

    # Load all faculties
    faculties = []

    # Preprare query
    sqlQueryFaculties = "SELECT * FROM Faculties"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryFaculties)

    # Run over the lines of the result and append to list
    for line in sqlRes:
        faculties.append([line[0], line[1]])

    # Close the connection to the database
    con.close()

    # Check if user already logged in
    if ('username' in session):
        return redirect('/')
    # If method post selected then register the user
    if (request.method == "POST"):
        # connect to db and check if username taken 
        con = sqlite3.connect(current_app.config['DB_NAME'])
        sqlQueryCheckExist = "SELECT * FROM Users WHERE UserName = (?)"
        sqlRes = con.execute(sqlQueryCheckExist, (request.form["username"],))
        record = sqlRes.fetchone()

        # Create user object
        newUser = User(request.form["username"],
                        request.form["fName"],
                        request.form["lName"],
                        request.form["password"],
                        request.form["institution"],
                        request.form["faculty"],
                        request.form["year"])
        
        # Check if the user is not already registered!
        if (record == None):
            # Validate the user
            valMessage = newUser.validateUser()

            valMessage = valMessage.replace('\n', '<br>')
            valMessage = Markup(valMessage)
            
            # Check if user is valid
            if (valMessage != ""):
                return render_template('register.html', massage = valMessage, institutions = institutions, faculties = faculties)

            # Insert the user into the table of users
            sqlQueryRegister = "INSERT INTO Users VALUES (?,?, ?, ?, ?, ?, ?, 0, 0)"
            con.execute(sqlQueryRegister, (newUser.getUsername(),
                                            newUser.getFName(),
                                            newUser.getLName(),
                                            newUser.getPassword(),
                                            newUser.getInstitutionID(),
                                            newUser.getFacultyID(),
                                            newUser.getStudyYear()))
            # Commit the changes in users table
            con.commit()
            
            # Create message
            massage = "User registered successfully!"
            
            # Add the user into the session variable
            session['username'] = newUser.getUsername()
        else:
            massage = "Username already taken please choose another!"
            return render_template('register.html', massage = massage, institutions = institutions, faculties = faculties)

        # Close the database connection
        con.close()

        return redirect('/')
    # Load and prepare the page
    else:
        return render_template('register.html', massage = "Please register", institutions = institutions, faculties = faculties)

@authentication_blueprint.route('/logout')
def logout():
    # Clean the session variable
    session.pop('username',None)
    session.pop('admin',None)

    # Redirect back to main screen
    return redirect('/')
