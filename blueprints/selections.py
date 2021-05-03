from flask import Blueprint, request, jsonify
from modules.selection import Selections

DB_NAME = "database.db"


selections_bp = Blueprint("selections_bp", __name__, template_folder="templates")


@selections_bp.route("/fetch/selection", methods=["POST"])
def api():
    selections = Selections(DB_NAME)
    current_selection = request.json
    next_selections = selections.get_selections(**current_selection)
    return jsonify(next_selections)
