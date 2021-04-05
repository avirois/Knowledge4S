"""Search api module."""
from flask import Blueprint, render_template, request, jsonify, session, current_app
from modules.selection import Selections
from modules.search import SearchEngine
import sqlite3

DB_NAME = "database.db"

search_blueprint = Blueprint("search_blueprint", __name__, template_folder="templates")
search_options_bp = Blueprint(
    "search_options_bp", __name__, template_folder="templates"
)

selections = Selections(DB_NAME)


@search_blueprint.route("/search", methods=["GET"])
def search_route():
    selections = Selections(DB_NAME)
    initial_selections = selections.get_selections()

    institutions = request.args.get("institutions", default=None, type=str)
    faculties = request.args.get("faculties", default=None, type=str)
    lecturers = request.args.get("lecturers", default=None, type=str)
    courses = request.args.get("courses", default=None, type=str)
    years = request.args.get("years", default=None, type=str)
    freetext = request.args.get("freetextsearch", default=None, type=str)

    if ('username' in session):
        if (institutions == None and faculties == None and lecturers == None and courses == None and years == None and freetext == None):
            search_res = {"files":[]}
            connection = sqlite3.connect(current_app.config['DB_NAME'])
            cur = connection.execute("SELECT InstitutelID,FacultyID,StudyYear FROM Users WHERE UserName = (?)",(session['username'],))
            for x in cur:
                institutions = request.args.get("institutions", x[0], type=str)
                faculties = request.args.get("faculties", x[1], type=str)
                lecturers = request.args.get("lecturers", default=None, type=str)
                courses = request.args.get("courses", default=None, type=str)
                years = request.args.get("years", x[2], type=str)
                freetext = request.args.get("freetextsearch", default=None, type=str)

            cur = connection.execute("SELECT * FROM Files WHERE InstituteID = ? AND FacultyID = ? ",(institutions,faculties,))
            for row in cur:
                search_res["files"].append(row)
            print(search_res)
            connection.close()
            return render_template(
                "search.html", **initial_selections, search_res=search_res
            )

    search_res = {"files": None}

    if institutions or faculties or lecturers or courses or years or freetext:
        search_res = SearchEngine(None).search(
            institutions, faculties, lecturers, courses, years, freetext
        )
    return render_template(
        "search.html", **initial_selections, search_res=search_res
    )


@search_options_bp.route("/search/fetch/selection", methods=["POST"])
def search_options_route():
    current_selection = request.json
    next_selections = selections.get_selections(**current_selection)
    return jsonify(next_selections)
