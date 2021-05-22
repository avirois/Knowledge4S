from flask import Blueprint, render_template,request,current_app,session, redirect,jsonify
import sqlite3,os

user_files_blueprint = Blueprint("user_files_blueprint", __name__, template_folder="templates")

def parse_file_time(string):
    tmp = string.split(" ")
    date = tmp[0]
    time = tmp[1]
    date = date.split("-")
    time = time.split(":")
    return "{}/{}/{} - {}:{}".format(date[2],date[1],date[0],time[0],time[1])

def getFiles():
    files = []
    con = sqlite3.connect(current_app.config['DB_NAME'])
    sqlQueryFiles = "SELECT FileID, FileName,DateUpload,DateModified,Approved FROM Files WHERE UserName = (?)"
    sqlRes = con.execute(sqlQueryFiles, (session.get('username'),))
    for line in sqlRes:
        files.append([line[0],line[1],parse_file_time(line[2]),parse_file_time(line[3]),line[4]])
    con.close()
    return files
 
@user_files_blueprint.route("/user_files",methods = ['GET', 'POST'])
def user_files_page():
    if (session.get('username') == None):
        return redirect('/')
    
    return render_template("user_files.html",files = getFiles())
        
    