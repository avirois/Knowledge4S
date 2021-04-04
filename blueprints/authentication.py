from flask import Blueprint, render_template, request, session, redirect, current_app, Markup, jsonify
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
        sqlQuryLogin = "SELECT * FROM Users WHERE username = (?)"
        sqlRes = con.execute(sqlQuryLogin,(request.form["username"],))
        record = sqlRes.fetchone()

        # Check if user exists
        if (record != None):
            # Create user object for current selected username
            usrLogin = User(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[8])

            # Check if password is correct and user is not banned
            if (usrLogin.validatePassword(request.form["password"])):
                # Check if user banned
                if (not usrLogin.getIsBanned()):
                    # Check if the user is admin or not
                    if (record[7] == 1):
                        session['admin'] = True
                    
                    # Save user name in session
                    session['username'] = usrLogin.getUsername()
                    massage = "Logged in successfuly!"

                    return redirect('/')
                # The user banned
                else:
                    massage = "Your user is banned!"
            # The password is incorrect
            else:
                massage = "Wrong password entered!"
        else:
            massage = "Wrong username entered!"

        # Close the connection to DB
        con.close()

        return render_template('login.html', massage = massage)
    # Get method mean open the page
    else:
        return render_template('login.html', massage = "Please fill the login form!")

@authentication_blueprint.route('/register',methods=['POST','GET'])
def register():
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
                return render_template('register.html', massage = valMessage, institutions = institutions)

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
            return render_template('register.html', massage = massage, institutions = institutions)

        # Close the database connection
        con.close()

        return redirect('/')
    # Load and prepare the page
    else:
        return render_template('register.html', massage = "Please register", institutions = institutions)

@authentication_blueprint.route('/faculties/<inst_ID>')
def facultyByInstitution(inst_ID):
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Create list of faculties in current institution
    facInInst = []

    # Preprare query
    sqlQueryFaculties = "SELECT * FROM Faculties WHERE FacultyID IN (SELECT FacultyID from FacIn WHERE InstitutionID = (?))"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryFaculties, (int(inst_ID),))

    # Run over the lines of the result and append to list
    for line in sqlRes:
        faculty = {}
        faculty['facID'] = line[0]
        faculty['facName'] = line[1]
        facInInst.append(faculty)

    # Close the connection to the database
    con.close()

    # Create json from the result list
    return jsonify({'facInst' : facInInst})

@authentication_blueprint.route('/logout')
def logout():
    # Clean the session variable
    session.pop('username',None)
    session.pop('admin',None)

    # Redirect back to main screen
    return redirect('/')
