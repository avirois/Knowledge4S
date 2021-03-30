"""Search api module."""
from flask import Blueprint, render_template, request, jsonify
from modules.selection import Selections

DB_NAME = "database.db"

search_blueprint = Blueprint("search_blueprint", __name__, template_folder="templates")
search_options_bp = Blueprint(
    "search_options_bp", __name__, template_folder="templates"
)

selections = Selections(DB_NAME)


@search_blueprint.route("/search", methods=["GET", "POST"])
def search_route():
    selections = Selections(DB_NAME)

    initial_selections = selections.get_selections()
    return render_template("search.html", **initial_selections)


@search_options_bp.route("/search/fetch/selection", methods=["POST"])
def search_options_route():
    current_selection = request.json
    next_selections = selections.get_selections(**current_selection)
    return jsonify(next_selections)
