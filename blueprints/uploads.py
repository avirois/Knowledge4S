from flask import Blueprint, render_template


upload_blueprint = Blueprint("upload_blueprint", __name__, template_folder="templates")


@upload_blueprint.route("/upload")
def upload():
    return render_template("upload.html")

	
# @upload_blueprint.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'