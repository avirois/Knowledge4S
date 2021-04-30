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
                                to user's institution and faculty.  
"""
import sys
import sqlite3
import PyPDF2
from typing import Union, Any
from pathlib import Path
from modules.search_by_free_text import DocumentsTermsFrequency
from modules.search_by_sql_queries import search_by_sql_queries

STORAGE_FOLDER = "storage"


def extract_text_from_document(database_name: str, document_id: Union[str, int]) -> str:
    """
    Collect text from document.

    Combine exctracted text from file (text/pdf) with text in title,
    file_name and description.
    """
    text = ""
    with sqlite3.connect(database_name) as con:
        res = con.execute(
            """
            select UserName, FileName, Title, Description
            from Files
            where FileID == ?
            """,
            (str(document_id),),
        ).fetchone()
        username = res[0]
        file_name = res[1]
        title = res[2]
        description = res[3]
        text = description + " " + file_name + " " + title + " " + username + " "

    storage_folder = Path(".", STORAGE_FOLDER)
    file_search_regex = str(document_id) + ".*"
    found = list(storage_folder.glob(file_search_regex))

    if len(found) != 1:
        if found:
            sys.exit("error have two same files with same id")
        else:
            sys.exit("error no file in storage start with: %d" % int(document_id))

    # File is .txt
    file = found[0]
    if ".txt" in str(file):
        with open(file, "r") as opened_file:
            text = text + opened_file.read().replace("\n", " ")

    # File is .pdf TODO
    if ".pdf" in str(file):
        extracted_txt = []
        with open(file, "rb") as opened_file:
            pdf_reader = PyPDF2.PdfFileReader(opened_file)
            num_of_pages = pdf_reader.getNumPages()
            for i in range(0, num_of_pages):
                pageObj = pdf_reader.getPage(i)
                extracted_txt.append(pageObj.extractText())
        print(extracted_txt)
        text = text + " ".join(extracted_txt)
    return text


def order_by_similarity_to(
    query: str, documents: list[Union[str, int]]
) -> tuple[str, ...]:
    """Warper aroud DocumentsTermsFrequency's order_by_similarity_to."""
    dtf = DocumentsTermsFrequency()
    return dtf.order_by_similarity_to(query, *documents)


def add_document(database_name: str, document_id: Union[str, int]) -> None:
    """Exatacting text from given document and adding to DocumentsTermsFrequency."""
    dtf = DocumentsTermsFrequency()
    dtf.add_document(
        document_id, extract_text_from_document(database_name, document_id)
    )


def init_search(database_name: str) -> DocumentsTermsFrequency:
    """
    Initialze DocumentsTermsFrequency.

    add all document from database to DocumentsTermsFrequency.
    """
    document_ids = list()
    with sqlite3.connect(database_name) as con:
        document_ids = con.execute("select FileID from Files").fetchall()

    for (id_,) in document_ids:
        add_document(database_name, id_)
    return DocumentsTermsFrequency()


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
        sorted_ids = order_by_similarity_to(freetext, ids)
        db_search_res.sort(key=lambda x: sorted_ids.index(str(x[5])))
    return db_search_res


def default_search_for_user(database_name: str, username:str) -> list[Any]:
    """Default search for username."""
    institute : str 
    faculty : str
    with sqlite3.connect(database_name) as con:
        cur = con.execute("""
                          SELECT Institutions.InstitutionName,Faculties.FacultyName
                          FROM Users,Institutions,Faculties
                          WHERE Users.UserName == ?
                                AND Institutions.InstitutionID == Users.InstitutelID
                                AND Faculties.facultyID == Users.FacultyID
                          """, (username,))
        (institute, faculty) = cur.fetchone()
    return search(database_name, institute, faculty, 'all', 'all', "all", "")
