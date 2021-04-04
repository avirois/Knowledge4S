from flask import Blueprint, render_template, session, redirect


controlpanel_blueprint = Blueprint("controlpanel_blueprint", __name__, template_folder="templates")


@controlpanel_blueprint.route("/controlpanel")
def controlpanel():
    # If user is not admin redirect him back to main page
    if (session.get("admin") == None):
        return redirect('/')

    return render_template("controlpanel.html")
