"""
Main search module.

This module combine the functionality of search_by_sql_queries and search_by_free_text
modules.

=> Functions:
    -> extract_text_from_document : extract all textual metadata and text from
                                    given file to sinle string.
    -> init_search : Populate DocumentsTermsFrequency object with documents from db
                     and return its instance.
    -> add_document : Add document id and documents text to DocumentsTermsFrequency.
    -> order_by_similarity_to : warper around search_by_free_text order_by_similarity_to
    -> search : search by search sql queries than sort quries acoring to freetext
                search logic (see freetext docs).

       search return format:
        list[                  # index # type
            tuple(             # ----- # ----
             Course name       #   0   #  str
            ,Date modified     #   1   #  str
            ,Date upload       #   2   #  str
            ,Description       #   3   #  str
            ,Faculty name      #   4   #  str
            ,File id           #   5   #  int
            ,File name         #   6   #  str
            ,Institution name  #   7   #  str
            ,Title             #   8   #  str
            ,User name         #   9   #  int
            )
        ]
    -> default_search_for_user: get db name and username preform acording 

"""
import sys
import sqlite3
import PyPDF2
from typing import Union, Any
from pathlib import Path
from modules.search_by_sql_queries import search_by_sql_queries
from modules.search_by_free_text import oreder_by__containing_freetext


def search(
    database_name: str,
    institutions: str,
    faculties: str,
    lecturers: str,
    courses: str,
    years: str,
    freetext: str,
) -> list[Any]:
    """
    Search.

    search by search sql queries than sort quries acoring to freetext
    search logic (see freetext docs).
    """
    db_search_res = search_by_sql_queries(
        database_name, institutions, faculties, lecturers, courses, years
    )
    if freetext not in ("", None):
        ids = [res[5] for res in db_search_res]
        sorted_ids = oreder_by__containing_freetext(freetext, ids)
        db_search_res.sort(key=lambda x: sorted_ids.index(str(x[5])))
    return db_search_res


def default_search_for_user(database_name: str, username: str) -> list[Any]:
    """Default search for username."""
    institute: str
    faculty: str
    with sqlite3.connect(database_name) as con:
        cur = con.execute(
            """
                          SELECT Institutions.InstitutionName,Faculties.FacultyName
                          FROM Users,Institutions,Faculties
                          WHERE Users.UserName == ?
                                AND Institutions.InstitutionID == Users.InstitutelID
                                AND Faculties.facultyID == Users.FacultyID
                          """,
            (username,),
        )
        (institute, faculty) = cur.fetchone()

    return search(database_name, institute, faculty, "all", "all", "all", "")
