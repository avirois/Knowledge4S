from flask import Blueprint, request, current_app, session, redirect
import sqlite3
from datetime import datetime

report_file = Blueprint("report_file", __name__, template_folder="templates")

@report_file.route("/report_file",methods = ['POST','GET'])
def report_file_1():
    if request.method == 'GET':
        if ('admin' in session):
            file_id = request.args.get('delete')
            try:
                con = sqlite3.connect(current_app.config['DB_NAME'])
                con.execute("DELETE FROM Reports WHERE ID=?",(file_id,))
                con.commit()
            except Exception as e:
                print(e)
            finally:
                con.close()
        redirect('/controlpanel')

    if request.method == 'POST':

        file_id = request.form['file_id']
        report_desc = request.form['desc']

        if ('username' in session):
            reported_by = session['username']
        else:
            reported_by = 'Guest'

        try:
            con = sqlite3.connect(current_app.config['DB_NAME'])
            con.execute("INSERT INTO Reports(FileId,Reporter,Date,Reason) VALUES (?,?,?,?)",(
                file_id,
                reported_by,
                datetime.now(),
                report_desc,
            ))
            con.commit()
        except Exception as e:
            print(e)
        finally:
            con.close()
    return redirect('/view?id='+file_id)