from flask import Blueprint, render_template, request, redirect, current_app, session
import sqlite3
from datetime import datetime
from static.classes.File import File

view_blueprint = Blueprint("view_blueprint", __name__, template_folder="templates")
delete_comment_blueprint = Blueprint(
    "delete_comment_blueprint", __name__, template_folder="templates"
)


@view_blueprint.route("/view", methods=["POST", "GET"])
def view():
    if request.method == "GET":
        file_id = request.args.get("id")
        # check that id is set
        if file_id is None:
            return redirect("/search")

        data = {}
        # fetch file data
        try:
            con = sqlite3.connect(current_app.config["DB_NAME"])
            cur = con.execute("SELECT * FROM Files WHERE FileID = ?", (file_id,))
            tmp = cur.fetchone()
            data["title"] = tmp[3]
            data["desc"] = tmp[4]
            data["username"] = tmp[1]
            data["id"] = tmp[0]
            data["filename"] = tmp[2]
            ftype = (tmp[2].split("."))[1]
            data["type"] = ftype
            data["inst"] = tmp[7]
            data["facu"] = tmp[8]
            data["course"] = tmp[9]
            data["date"] = parse_file_time(tmp[5])
            data["preapproved"] = tmp[10]

            # Check if file not approved yet move the user if not admin to main page
            if session.get("admin") == None and data["preapproved"] == 0:
                return redirect("/")

            # get instetution name
            cur = con.execute(
                "SELECT InstitutionName FROM Institutions WHERE InstitutionID = ?",
                (data["inst"],),
            )
            tmp = cur.fetchone()
            data["inst"] = tmp[0]

            # get faculty name
            cur = con.execute(
                "SELECT FacultyName FROM Faculties WHERE FacultyID = ?", (data["facu"],)
            )
            tmp = cur.fetchone()
            data["facu"] = tmp[0]

            # get course name
            cur = con.execute(
                "SELECT CourseName FROM Courses WHERE CourseID = ?", (data["course"],)
            )
            tmp = cur.fetchone()
            data["course"] = tmp[0]

            # get comments
            cur = con.execute(
                "SELECT UserName,Date,Comment,ID FROM Comments WHERE FileID = ?",
                (data["id"],),
            )
            data["comments"] = []
            for row in cur:
                tmp = (row[0], parse_file_time(row[1]), row[2], row[3])
                data["comments"].append(tmp)

        except Exception as e:
            print(e)
            con.close()
            return redirect("/")
        finally:
            con.close()
        return render_template("view.html", data=data)

    if request.method == "POST":
        if session.get("username") == None:
            return redirect("/")
        else:
            comment = request.form["comment"]
            file_id = request.form["file_id"]
            if comment != "":
                try:
                    con = sqlite3.connect(current_app.config["DB_NAME"])
                    cur = con.execute(
                        "INSERT into Comments (FileID,Date,UserName,Comment) VALUES (?,?,?,?)",
                        (
                            file_id,
                            datetime.now(),
                            session["username"],
                            comment,
                        ),
                    )
                    con.commit()
                except Exception as e:
                    print(e)
                finally:
                    con.close()
            return redirect("/view?id={}".format(file_id))


@delete_comment_blueprint.route("/delete_comment/<id>", methods=["GET"])
def delete_comment(id):
    # check admin session
    if session.get("admin") == None:
        return redirect("/")
    # delete the comment
    try:
        con = sqlite3.connect(current_app.config["DB_NAME"])
        con.execute("DELETE FROM Comments WHERE ID = ?", (id,))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()
    post_id = request.args.get("post")
    return redirect("/view?id={}".format(post_id))


def parse_file_time(string):
    tmp = string.split(" ")
    date = tmp[0]
    time = tmp[1]
    date = date.split("-")
    time = time.split(":")
    return "{}/{}/{} - {}:{}".format(date[2], date[1], date[0], time[0], time[1])


def editTitleDB(fileUpdt):
    # Connect to database
    con = sqlite3.connect(current_app.config["DB_NAME"])

    # Prepare the query
    sqlQueryUpdateFile = "UPDATE Files SET Title = (?) WHERE FileID = (?)"
    con.execute(sqlQueryUpdateFile, (fileUpdt.getTitle(), fileUpdt.getFileID()))

    # Commit the changes
    con.commit()

    # Close the connection to the database
    con.close()


@delete_comment_blueprint.route("/edit_title/<id>", methods=["GET", "POST"])
def edit_title(id):
    # connect to db
    con = sqlite3.connect(current_app.config["DB_NAME"])

    # Preprare query
    queryUser = "SELECT UserName FROM Files WHERE FileID = (?)"

    res = con.execute(queryUser, (int(id),))

    # Fetch the result
    record = res.fetchone()

    # Close the connection to the database
    con.close()

    # check admin session
    if (session.get("admin") == None) and (session.get("username") != record[0]):
        return redirect("/")

    # If method post selected then need to edit the title
    if request.method == "POST":
        # connect to db
        con = sqlite3.connect(current_app.config["DB_NAME"])

        # Save the ID of the file
        fileID = int(id)

        # Get new file title from the form
        newFileTitle = request.form["title"]

        # Create file object
        newFile = File(fileID, Title=newFileTitle)

        # Update the title to the new one
        editTitleDB(newFile)

    return redirect("/view?id=" + str(fileID))


def editDescriptionDB(fileUpdt):
    # Connect to database
    con = sqlite3.connect(current_app.config["DB_NAME"])

    # Prepare the query
    sqlQueryUpdateFile = "UPDATE Files SET Description = (?) WHERE FileID = (?)"
    con.execute(sqlQueryUpdateFile, (fileUpdt.getDescription(), fileUpdt.getFileID()))

    # Commit the changes
    con.commit()

    # Close the connection to the database
    con.close()


@delete_comment_blueprint.route("/edit_description/<id>", methods=["GET", "POST"])
def edit_description(id):
    # connect to db
    con = sqlite3.connect(current_app.config["DB_NAME"])

    # Preprare query
    queryUser = "SELECT UserName FROM Files WHERE FileID = (?)"

    res = con.execute(queryUser, (int(id),))

    # Fetch the result
    record = res.fetchone()

    # Close the connection to the database
    con.close()

    # check admin session
    if (session.get("admin") == None) and (session.get("username") != record[0]):
        return redirect("/")

    # If method post selected then need to edit the description
    if request.method == "POST":
        # connect to db
        con = sqlite3.connect(current_app.config["DB_NAME"])

        # Save the ID of the file
        fileID = int(id)

        # Get new file description from the form
        newFileDesc = request.form["description"]

        # Create file object
        newFile = File(fileID, Description=newFileDesc)

        # Update the description to the new one
        editDescriptionDB(newFile)

    return redirect("/view?id=" + str(fileID))
