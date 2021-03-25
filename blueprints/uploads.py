from flask import Blueprint, render_template,request
from werkzeug.utils import secure_filename
import os

upload_blueprint = Blueprint("upload_blueprint", __name__, template_folder="templates")
UPLOAD_FOLDER ='storage/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_blueprint.route("/upload",methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            ##TODO add file info to db (course,school,fucilty,data,time,uploadbywhom)
            return render_template("upload.html",data = { "msg" : "file uploaded successfully"})
        else:
            return render_template("upload.html",data = { "msg" : "file type is not supported."})
    else:
        return render_template("upload.html", data = {"msg" : ""})
