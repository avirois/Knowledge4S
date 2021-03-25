"""Search api module."""
import sqlite3
from flask import Blueprint, render_template, current_app


search_blueprint = Blueprint("search_blueprint", __name__, template_folder="templates")


@search_blueprint.route("/search", methods=["GET", "POST"])
def route():
    return render_template("search.html")
