from flask import Flask, render_template, request, session, redirect
import sqlite3
from blueprints.index import index_blueprint

app = Flask(__name__)

# Configure secret key inorder to allow login
app.secret_key = b'\xf5\xe4\xabr\x89\xd9#^D@0\xae[R1\xcf'

app.register_blueprint(index_blueprint)

# Database name
app.config['DB_NAME'] = 'database.db'

@app.route('/login',methods=['POST','GET'])
def login():
    # Check if user already logged in
    if ('username' in session):
        return redirect('/')
    # Check if post method selected therfore need to login the user
    if request.method == "POST":
        # Connect to database and check if user exists
        con = sqlite3.connect(app.config['DB_NAME'])
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

@app.route('/register',methods=['POST','GET'])
def register():
    # Check if user already logged in
    if ('username' in session):
        return redirect('/')
    # If method post selected then register the user
    if (request.method == "POST"):
        # connect to db and check if username taken 
        con = sqlite3.connect(app.config['DB_NAME'])
        sqlQueryCheckExist = "SELECT * FROM Users WHERE UserName = (?)"
        sqlRes = con.execute(sqlQueryCheckExist, (request.form["username"],))
        record = sqlRes.fetchone()
        
        # Check if the user is not already registered!
        if (record == None):
            # Insert the user into the table of users
            sqlQueryRegister = "INSERT INTO Users VALUES (?,?, ?, ?, ?, ?, ?, 0, 0)"
            con.execute(sqlQueryRegister, (request.form["username"],
                                            request.form["fName"],
                                            request.form["lName"],
                                            request.form["password"],
                                            request.form["institution"],
                                            request.form["faculty"],
                                            request.form["year"]))
            # Commit the changes in users table
            con.commit()
            
            # Create message
            massage = "User registered successfully!"
            
            # Add the user into the session variable
            session['username'] = request.form["username"]
        else:
            massage = "Username already taken please choose another!"
            return render_template('register.html', massage = massage)

        # Close the database connection
        con.close()

        return redirect('/')
    # Load and prepare the page
    else:
        con = sqlite3.connect(app.config['DB_NAME'])

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

        return render_template('register.html', massage = "Please register", institutions = institutions, faculties = faculties)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
