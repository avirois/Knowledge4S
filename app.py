from flask import Flask, render_template, request, session, redirect,current_app
from blueprints.index import index_blueprint
from blueprints.uploads import upload_blueprint,UPLOAD_FOLDER
from blueprints.authentication import authentication_blueprint
from blueprints.controlpanel import controlpanel_blueprint
import sqlite3,base64,os,datetime
from blueprints.manageInstitution import inst_manage_blueprint
from blueprints.manageFaculty import fac_manage_blueprint

app = Flask(__name__)

app.register_blueprint(index_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(controlpanel_blueprint)
app.register_blueprint(inst_manage_blueprint)
app.register_blueprint(fac_manage_blueprint)

# Configure Upload Folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database name
app.config['DB_NAME'] = 'database.db'

# Configure secret key inorder to allow login
app.secret_key = b'\xf5\xe4\xabr\x89\xd9#^D@0\xae[R1\xcf'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)