"""
Search by sql query module.

Functions:
-> is_not_selected:
   Check if field not seleced.
     (str*) -> bool

-> search_by_sql_queries:
    The core function of the module,
    this function preform a query according to given parameters.
    When some of the input in missing or "" return empty list
    and not preforming the query.

    Input:
    ------
    ( database_name, institutions, faculties ,lecturer ,course ,year)

    Return format:
    -------------
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

    Example:
    --------
    >>> search_by_sql_queries("database.db", "A", "math", "all", "all", "all")
    [
        (
            "Calculus",
            "1.1.2021",
            "1.1.2021",
            "special number",
            "math",
            1,
            "F1.txt",
            "A",
            "title-math",
            "Yosi",
        )
    ]
    >>> search_by_sql_queries("database.db", "all", "all", "all")
    []
"""
import sqlite3
from typing import Union, Any, cast


def is_not_selected(*args: Union[str, None]) -> bool:
    """Check if field not seleced."""
    for arg in args:
        if arg in ("", None):
            return True
    return False


def search_by_sql_queries(
    database_name: str,
    institutions: Union[str, None],
    faculties: Union[str, None],
    lecturer: Union[str, None],
    course: Union[str, None],
    year: Union[str, None],
) -> list[Any]:
    """
    Perform Search according to given parameters.

    Return empty list when missing parameters
    Expected parameters are words for the query and the word 'all'.
    The word 'all' is passed as parameter meaning query all from
    table its variable name representing.

    Return format:
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
    """
    if is_not_selected(institutions, faculties, lecturer, course, year):
        return list()

    # from here institutions, faculties, lecturer, course, year are only str
    institutions = cast(str, institutions)
    faculties = cast(str, faculties)
    lecturer = cast(str, lecturer)
    course = cast(str, course)
    year = cast(str, year)

    with sqlite3.connect(database_name) as con:
        args: list[Union[str, int]] = []
        select = """
        SELECT
            Courses.CourseName
            ,Files.DateModified
            ,Files.DateUpload
            ,Files.Description
            ,Faculties.FacultyName
            ,Files.FileID
            ,Files.FileName
            ,Institutions.InstitutionName
            ,Files.Title
            ,Files.UserName
        """
        from_ = """
        FROM Files, Institutions, Faculties, Lecturers, Courses
        """
        where = """
        WHERE
        Files.InstituteID == Institutions.InstitutionID
        AND Files.FacultyID == Faculties.FacultyID
        AND Files.CourseID == Courses.CourseID
        AND Courses.LecturerID == Lecturers.LecturerID
        """
        if institutions != "all":
            where = where + " AND Institutions.InstitutionName == ?  "
            args.append(institutions)
        if faculties != "all":
            where = where + " AND Faculties.FacultyName == ?  "
            args.append(faculties)
        if lecturer != "all":
            where = where + " AND Lecturers.LecturerName == ?  "
            args.append(lecturer)
        if course != "all":
            where = where + " AND Courses.CourseName == ?  "
            args.append(course)
        if year != "all":
            where = where + " AND Courses.Year == ?  "
            args.append(int(year))
        cur = con.execute(select + from_ + where, args)
        return cur.fetchall()
