"""Search api module."""
from flask import Blueprint, render_template, request, session
from modules.search import search, default_search_for_user
from modules.selection import Selections

DB_NAME = "database.db"

search_blueprint = Blueprint("search_blueprint", __name__, template_folder="templates")

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

    if (
        "username" in session
        and institutions is None
        and faculties is None
        and lecturers is None
        and courses is None
        and years is None
        and freetext is None
    ):
        search_res = default_search_for_user(DB_NAME, session["username"])
        return render_template(
            "search.html", **initial_selections, search_res=search_res
        )

    search_res = search(
        DB_NAME, institutions, faculties, lecturers, courses, years, freetext
    )

    return render_template(
        "search.html", **initial_selections, freetext=freetext, search_res=search_res
    )
