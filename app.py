"""Main module from here the app starts."""
from flask import Flask
from blueprints.authentication import authentication_blueprint
from blueprints.controlpanel import controlpanel_blueprint
from blueprints.user import user_blueprint
from blueprints.index import index_blueprint
from blueprints.manageFaculty import fac_manage_blueprint
from blueprints.manageInstitution import inst_manage_blueprint
from blueprints.search import search_blueprint, search_options_bp
from blueprints.uploads import upload_blueprint,UPLOAD_FOLDER
from blueprints.manageCourse import cour_manage_blueprint
from blueprints.view import view_blueprint,delete_comment_blueprint
from blueprints.serve_file import serve_blueprint
from blueprints.manageUser import user_manage_blueprint
from blueprints.user_files import user_files_blueprint


app = Flask(__name__)
app.register_blueprint(index_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(search_options_bp)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(controlpanel_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(inst_manage_blueprint)
app.register_blueprint(fac_manage_blueprint)
app.register_blueprint(cour_manage_blueprint)
app.register_blueprint(view_blueprint)
app.register_blueprint(serve_blueprint)
app.register_blueprint(user_manage_blueprint)
app.register_blueprint(delete_comment_blueprint)
app.register_blueprint(user_files_blueprint)

app.config["DB_NAME"] = "database.db"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = b"\xf5\xe4\xabr\x89\xd9#^D@0\xae[R1\xcf"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
