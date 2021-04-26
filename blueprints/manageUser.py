from flask import Blueprint, render_template, request, session, redirect, current_app, Markup, jsonify
import sqlite3
import os
from static.classes.User import User
from static.classes.Admin import Admin

user_manage_blueprint = Blueprint("manage_user_blueprint", __name__, template_folder="templates")

def getUsersInfo():
    # List of users
    lstUsers = []

    # Connect to database
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Prepare the query
    sqlQury = "SELECT * FROM Users"

    # Run the query to get user data
    sqlRes = con.execute(sqlQury)

    # Run over the lines of the result and append to list
    for line in sqlRes:
        if line[7] == 0:
            lstUsers.append(User(line[0], line[1], line[2], None, line[4], line[5], line[6], line[8], line[9]))
        else:
            lstUsers.append(Admin(line[0], line[1], line[2], None, line[4], line[5], line[6], line[8], line[9]))

    # Close the connection to the database
    con.close()

    return (lstUsers)

@user_manage_blueprint.route('/manage_users', methods=['GET'])
def manage_user():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    return render_template('manage_users.html', users = getUsersInfo())

@user_manage_blueprint.route('/ban_unban/<user>', methods=['GET'])
def ban_unban_user(user):
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # Connect to database
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Check if user exists in Users table
    sqlQueryCheckExist = "SELECT * FROM Users WHERE UserName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (user,))
    record = sqlRes.fetchone()
    
    # If user exists ban or unban him
    if (record != None):
        # Get user is banned status
        isBanned = record[8]

        # Change banned status
        ban_unban = (isBanned + 1) % 2

        sqlBanUser = "UPDATE Users SET IsBanned = (?)  WHERE UserName = (?)"
        con.execute(sqlBanUser, (ban_unban, user))
    
    # Commit the changes in users table
    con.commit()
    
    # Close database
    con.close()

    return redirect('/manage_users')

@user_manage_blueprint.route('/grant_revoke_admin/<user>', methods=['GET'])
def grant_revoke_admin(user):
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    # Connect to database
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Check if user exists in Users table
    sqlQueryCheckExist = "SELECT * FROM Users WHERE UserName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (user,))
    record = sqlRes.fetchone()
    
    # If user exists grant or revoke admin role
    if (record != None):
        # Get user is banned status
        isAdmin = record[7]

        # Change banned status
        grant_revoke = (isAdmin + 1) % 2

        sqlBanUser = "UPDATE Users SET Role = (?)  WHERE UserName = (?)"
        con.execute(sqlBanUser, (grant_revoke, user))
    
    # Commit the changes in users table
    con.commit()
    
    # Close database
    con.close()

    return redirect('/manage_users')