from flask import Blueprint, send_from_directory


serve_blueprint = Blueprint("serve_blueprint", __name__, template_folder="templates")
serve_backup_blueprint = Blueprint(
    "serve_backup_blueprint", __name__, template_folder="templates"
)


@serve_blueprint.route("/storage/<id>")
def serve(id):
    return send_from_directory("storage/", id)


@serve_backup_blueprint.route("/storage/backup/<filename>")
def serve(filename):
    return send_from_directory("storage/backup", filename)
