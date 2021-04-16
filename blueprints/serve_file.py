from flask import Blueprint,send_from_directory


serve_blueprint = Blueprint("serve_blueprint", __name__, template_folder="templates")


@serve_blueprint.route("/storage/<id>")
def serve(id):
    return send_from_directory('storage/',id)   