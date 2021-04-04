from flask import Blueprint, render_template


user_blueprint = Blueprint("user_blueprint", __name__, template_folder="templates")


@user_blueprint.route("/user/<name>")
def index(name):
    return render_template("user.html",data = name)