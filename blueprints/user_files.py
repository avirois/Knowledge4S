from flask import Blueprint, render_template,request,current_app,session, redirect,jsonify
import sqlite3,os

user_files_blueprint = Blueprint("user_files_blueprint", __name__, template_folder="templates")

def getFiles():
    files = []
    con = sqlite3.connect(current_app.config['DB_NAME'])
    sqlQueryFiles = "SELECT FileID, FileName,DateUpload,DateModified FROM Files WHERE UserName = (?)"
    sqlRes = con.execute(sqlQueryFiles, (session.get('username'),))
    for line in sqlRes:
        files.append([line[0],line[1],line[2],line[3]])
    con.close()
    return files



@user_files_blueprint.route("/user_files",methods = ['GET', 'POST'])
def user_files_page():
    if (session.get('username') == None):
        return redirect('/')
    
    return render_template("user_files.html",files = getFiles())
        
    