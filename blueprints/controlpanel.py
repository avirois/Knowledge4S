from flask import Blueprint, render_template


controlpanel_blueprint = Blueprint("controlpanel_blueprint", __name__, template_folder="templates")


@controlpanel_blueprint.route("/controlpanel")
def controlpanel():
    return render_template("controlpanel.html")
