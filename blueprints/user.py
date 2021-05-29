from flask import Blueprint, render_template, session, current_app, request, redirect
from static.classes.User import User, encryptPassword, decryptPassword
from static.classes.Admin import Admin
import sqlite3

user_blueprint = Blueprint("user_blueprint", __name__, template_folder="templates")

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

def getUserInfo(name):
    # Connect to database and check if user exists
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Prepare the query
    sqlQury = "SELECT * FROM Users WHERE username = (?)"

    # Run the query to get user data
    sqlRes = con.execute(sqlQury,(name,))

    # Fetch the result
    record = sqlRes.fetchone()

    # Create user object for current selected username
    infoUser = None

    # Check if user exists
    if (record != None):
        # Create user object for current selected username
        infoUser = User(record[0], record[1], record[2], None, record[4], record[5], record[6], record[8], email=record[9])

    # Close the connection to the database
    con.close()

    return (infoUser)

def getAdminsInfo():
    # Set admin role
    adminRole = 1

    # List of admins
    lstAdmins = []

    # Connect to database and check if user exists
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Prepare the query
    sqlQury = "SELECT * FROM Users WHERE role = ?"

    # Run the query to get user data
    sqlRes = con.execute(sqlQury,(adminRole,))

    # Run over the lines of the result and append to list
    for line in sqlRes:
        lstAdmins.append(Admin(line[0], line[1], line[2], None, line[4], line[5], line[6], line[8], line[9]))

    # Close the connection to the database
    con.close()

    return (lstAdmins)

def updatePassword(userUpdate):
    # Connect to database and check if user exists
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Prepare the query
    sqlQueryUpdateUser = "UPDATE Users SET Password = (?)  WHERE UserName = (?)"

    # Run the query to get user data
    con.execute(sqlQueryUpdateUser,(encryptPassword(userUpdate.getPassword()),
                                     userUpdate.getUsername()))

    # Commit the changes
    con.commit()

    # Close the connection to the database
    con.close()

def updateUserBio(userUpdate):
    # Connect to database and check if user exists
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Prepare the query
    sqlQueryUpdateUser = "UPDATE Users SET FirstName = (?), LastName = (?), InstitutelID = (?), FacultyID =(?), StudyYear = (?), Email = (?)  WHERE UserName = (?)"

    # Run the query to get user data
    con.execute(sqlQueryUpdateUser,(userUpdate.getFName(), userUpdate.getLName(), userUpdate.getInstitutionID(),
                                     userUpdate.getFacultyID(), userUpdate.getStudyYear(), userUpdate.getEmail(),
                                     userUpdate.getUsername()))

    # Commit the changes
    con.commit()

    # Close the connection to the database
    con.close()

def parse_file_time(string):
    tmp = string.split(" ")
    date = tmp[0]
    time = tmp[1]
    date = date.split("-")
    time = time.split(":")
    return "{}/{}/{} - {}:{}".format(date[2],date[1],date[0],time[0],time[1])

def getNotifications(name):
    data = {
        'data': [],
        'new' : 0
    }
    try:
        con = sqlite3.connect(current_app.config['DB_NAME'])
        cur = con.execute("SELECT Date,MSG,Viewed FROM Notification WHERE User = ? ORDER BY Date DESC LIMIT 20",(name,))
        for row in cur:
            data['data'].append((parse_file_time(row[0]),row[1]))
            if row[2] == 0:
                data['new'] = data['new'] + 1

        con.execute("UPDATE Notification SET Viewed = 1 WHERE User = ?",(name,))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()
    return data

@user_blueprint.route("/user/<name>")
def index(name):
    
    # Load current user data
    usr = getUserInfo(name)
    notifications = getNotifications(name)
    
    return render_template("user.html", data = name, user = usr, notifications = notifications)

@user_blueprint.route("/edit_bio/<name>",methods=['POST','GET'])
def edit_bio(name):
    # Check if user already logged in
    if ('username' not in session):
        return redirect('/')

    # Check if editing not current user
    if (session.get('username') != name):
        return redirect('/')

    # Get institutions
    institutions = getInstitutions()

    # Load current user data
    usr = getUserInfo(name)

    # Check if post method selected therfore need to login the user
    if (request.method == "POST"):
        
        # Update user bio
        usrUpdate = User(name,
                        request.form["fName"],
                        request.form["lName"],
                        None,
                        request.form["institution"],
                        request.form["faculty"],
                        request.form["year"],
                        email = request.form["email"])

        # Validate the user before update
        msgValidateEdit = usrUpdate.validateEditBio()

        if (msgValidateEdit == ""):
            # Update user info
            updateUserBio(usrUpdate)

            return render_template("user.html", data = name, user = usrUpdate)
        else:
            return render_template("edit_bio.html", data = name, user = usr, institutions = institutions, massage = msgValidateEdit)

    # Method get
    else:
        return render_template("edit_bio.html", data = name, user = usr, institutions = institutions)

@user_blueprint.route("/change_pass/<name>",methods=['POST','GET'])
def change_pass(name):
    # Check if user already logged in
    if ('username' not in session):
        return redirect('/')

    # Check if editing not current user
    if (session.get('username') != name):
        return redirect('/')
    
    # Load current user data
    usr = getUserInfo(name)

    # Check if post method selected therfore need to login the user
    if (request.method == "POST"):

        # Check if password and confirm are not same
        if (request.form["password"] != request.form["confirmPass"]):
            return render_template("change_password.html", data = name, massage="Password confirm is incorrect!")
        
        # Set new password
        usr.setPassword(request.form["password"])

        # Validate the user password
        msgVal = usr.validateUser()

        # Check the message of validation
        if (msgVal != ""):
            return render_template("change_password.html", data = name, massage=msgVal)

        # Change password in DB
        updatePassword(usr)

        # Return to user page
        return redirect('/user/' + name)
    # Method get
    else:
        return render_template("change_password.html", data = name)

@user_blueprint.route("/admins_info",methods=['GET'])
def admins_info():
    # Get information about all admins in the system
    lstAdmins = getAdminsInfo()

    return render_template("admins_page.html", admins = lstAdmins)
