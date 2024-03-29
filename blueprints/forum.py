from flask import Blueprint, render_template, request, session, redirect, current_app, Markup, jsonify
import sqlite3
from static.classes.Course import Course

forum_blueprint = Blueprint("forum_blueprint", __name__, template_folder="templates")

@forum_blueprint.route('/forum',methods=['GET'])
def forum():
    data = dataForAllInst()
    return render_template('forum.html', data = data)

def dataForAllInst():
    con = sqlite3.connect(current_app.config['DB_NAME'])

    # Create list of objects
    institutions = []
    facInInst = []
    coursInfac = []

    # Preprare query
    sqlQueryInstitutions = "SELECT * FROM Institutions"

    # Run the query and save result
    sqlRes = con.execute(sqlQueryInstitutions)

    # Run over institutions
    for inst in sqlRes:
        
        institute = {}
        institute['instID'] = inst[0]
        institute['instName'] = inst[1]

        # Preprare query
        sqlQueryFaculties = "SELECT * FROM Faculties WHERE FacultyID IN (SELECT FacultyID from FacIn WHERE InstitutionID = (?))"

        # Run the query and save result
        sqlRes = con.execute(sqlQueryFaculties, (int(inst[0]),))

        # Run over the lines of the result and append to list
        for fac in sqlRes:
            faculty = {}
            faculty['facID'] = fac[0]
            faculty['facName'] = fac[1]

            # Preprare query
            sqlQueryCourses = "SELECT CourseID, CourseName FROM Courses WHERE LecturerID IN (SELECT LecturerID from Lecturers WHERE FacultyID = (?) and InstitutionID = (?))"

            # Run the query and save result
            sqlRes = con.execute(sqlQueryCourses, (int(fac[0]), int(inst[0])))

            # Run over the lines of the result and append to list
            for cor in sqlRes:
                course = {}
                course["courID"] = cor[0]
                course["courName"] = cor[1]
                coursInfac.append(course)

            # Add courses to faculty
            faculty['courses'] = coursInfac

            # Append faculty to faculties list
            facInInst.append(faculty)
            
            # Reset courses in faculty
            coursInfac = []

        # Add faculties in institution
        institute['faculties'] = facInInst

        # Append institute to institutions list
        institutions.append(institute)

        # Reset faculties of institutions
        facInInst = []

    # Close the connection to the database
    con.close()

    # Create json from the result list
    return (institutions)

@forum_blueprint.route('/course_forum/<courID>', methods=['GET', 'POST'])
def forumOfCourse(courID):
    curCourse = Course(courID)

    # Check if get method selected or post for update
    if request.method == 'GET':
        return render_template('course_forum.html', course = curCourse.courseNameByID(), courseID = courID, messages = curCourse.getMessagesOfCourse())
    else:
        forumComment = request.form['forumComment']
        preMessageID = request.form['preMessage']
        
        # Check if entered comment
        if forumComment != "":
            # Create the comment in the DB
            curCourse.addMessageToCourse(forumComment, session.get("username"), preMessageID)

            return redirect('/course_forum/' + courID)

@forum_blueprint.route("/delete_message/<id>", methods = ['GET'])
def delete_message(id):
    # Get coures id from paramters
    courseID = request.args.get("courseID")

    # Create temp course to delete the message
    curCourse = Course(courseID)
    
    # Get username info of the current comment
    username = curCourse.getSpecificMessageForum(id).getUserName()

    # check admin session 
    if ((session.get("admin") == None) and (session.get("username") != username)):
        return redirect('/')
    
    # delete the message
    curCourse.deleteMessageForum(id)

    return redirect('/course_forum/{}'.format(courseID))

@forum_blueprint.route("/edit_forum_message/<id>", methods = ['POST'])
def edit_forum_message(id):
    # Get coures id from paramters
    courseID = request.args.get("courseID")

    # Create temp course to delete the message
    curCourse = Course(courseID)

    # Get username info of the current comment
    username = curCourse.getSpecificMessageForum(id).getUserName()

    # check admin session 
    if ((session.get("admin") == None) and (session.get("username") != username)):
        return redirect('/')
    
    # delete the message
    curCourse.editMessageForum(id, request.form['newComment'])

    return redirect('/course_forum/{}'.format(courseID))