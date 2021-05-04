"""Search api module."""
from flask import Blueprint, render_template


about_bp = Blueprint("about_bp", __name__, template_folder="templates")


@about_bp.route("/about")
def show():
    return render_template("about.html")
