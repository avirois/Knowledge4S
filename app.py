"""Main module from here the app starts."""
import os
from flask import Flask
from blueprints.about import about_bp
from blueprints.authentication import authentication_blueprint
from blueprints.controlpanel import (
    controlpanel_blueprint,
    controlpanel_approve_blueprint,
    controlpanel_reject_blueprint,
)
from blueprints.delete import delete_blueprint
from blueprints.delete_my_files import delete_my_file_blueprint
from blueprints.forum import forum_blueprint
from blueprints.index import index_blueprint
from blueprints.lastUpdates import last_updates_blueprint
from blueprints.manageCourse import cour_manage_blueprint
from blueprints.manageFaculty import fac_manage_blueprint
from blueprints.manageInstitution import inst_manage_blueprint
from blueprints.manageLecturers import manage_lecturers, add_lecturer, remove_lecturer
from blueprints.manageTypes import manage_types_blueprint
from blueprints.manageUser import user_manage_blueprint
from blueprints.modification import modification_blueprint
from blueprints.report import report_file
from blueprints.report_status import my_reports_blueprint
from blueprints.search import search_blueprint
from blueprints.selections import selections_bp
from blueprints.serve_file import serve_blueprint, serve_backup_blueprint
from blueprints.update import update_my_file_blueprint
from blueprints.uploads import upload_blueprint, UPLOAD_FOLDER, type_list
from blueprints.user_files import user_files_blueprint
from blueprints.user import user_blueprint
from blueprints.view_backup import view_backup_blueprint
from blueprints.view import view_blueprint, delete_comment_blueprint

app = Flask(__name__)

app.register_blueprint(about_bp)
app.register_blueprint(add_lecturer)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(controlpanel_approve_blueprint)
app.register_blueprint(controlpanel_blueprint)
app.register_blueprint(controlpanel_reject_blueprint)
app.register_blueprint(cour_manage_blueprint)
app.register_blueprint(delete_blueprint)
app.register_blueprint(delete_comment_blueprint)
app.register_blueprint(delete_my_file_blueprint)
app.register_blueprint(fac_manage_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(inst_manage_blueprint)
app.register_blueprint(last_updates_blueprint)
app.register_blueprint(manage_lecturers)
app.register_blueprint(manage_types_blueprint)
app.register_blueprint(modification_blueprint)
app.register_blueprint(my_reports_blueprint)
app.register_blueprint(remove_lecturer)
app.register_blueprint(report_file)
app.register_blueprint(search_blueprint)
app.register_blueprint(selections_bp)
app.register_blueprint(serve_backup_blueprint)
app.register_blueprint(serve_blueprint)
app.register_blueprint(type_list)
app.register_blueprint(update_my_file_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(user_files_blueprint)
app.register_blueprint(user_manage_blueprint)
app.register_blueprint(view_backup_blueprint)
app.register_blueprint(view_blueprint)

app.config["DB_NAME"] = "database.db"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = b"\xf5\xe4\xabr\x89\xd9#^D@0\xae[R1\xcf"

# Create storage folders if not exists
try:
    os.mkdir("storage")
except FileExistsError as e:
    pass

# Create backup folder if not exsits
try:
    os.mkdir(os.path.join("storage","backup"))
except FileExistsError as e:
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
