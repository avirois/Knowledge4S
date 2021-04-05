"""SearchEngine."""
import sys
from pathlib import Path
import sqlite3
import PyPDF2
from modules.free_text import FreeTextSearchEngine
from modules.util import Singleton

STORAGE_FOLDER = "storage"


class SearchEngine(metaclass=Singleton):
    """Eager initialization singeton search engine."""

    def __init__(self, database_name):
        """
        Create instance.

        Create SearchEngine instance with database_name,
        and initialse the free text search engine.
        """
        self.db_name = database_name
        self.free_text_engine = FreeTextSearchEngine(self.get_all_documents_txt())

    def add_document(self, document_id, description, file_name, title):
        """
        Add document to the search engine.

        This will allow document to be found via free text search.
        """
        self.free_text_engine.add_document(
            document_id,
            self.document2text(document_id, description, file_name, title),
        )

    def get_all_documents_txt(self):
        """Exctract text  information from stored documents."""
        documents_text = dict()
        files_data = list()
        with sqlite3.connect(self.db_name) as con:
            files_cur: sqlite3.Cursor = con.execute(
                "SELECT FileID, Description, FileName, Title FROM Files"
            )
            files_data = files_cur.fetchall()

        for (f_id, description, file_name, title) in files_data:
            documents_text[str(f_id)] = self.document2text(
                f_id, description, file_name, title
            )
        return documents_text

    def document2text(self, document_id, description, file_name, title):
        """
        Collect text.

        Combine exctracted text from file (text/pdf) with text in title,
        file_name and description.
        """
        text = description + " " + file_name + " " + title
        storage_folder = Path(".", STORAGE_FOLDER)
        file_search_regex = str(document_id) + ".*"
        found = list(storage_folder.glob(file_search_regex))
        if len(found) != 1:
            sys.exit("error have two same files with same id")
        file = found[0]
        if ".txt" in str(file):
            with open(file, "r") as f:
                text = text + f.read().replace("\n", "")
        if ".pdf" in str(file):
            extracted_txt = []
            with open(file, "rb") as f:
                pdfReader = PyPDF2.PdfFileReader(f)
                numOfPages = pdfReader.getNumPages()
                for i in range(0, numOfPages):
                    pageObj = pdfReader.getPage(i)
                    extracted_txt.append(pageObj.extractText())
            print(extracted_txt)
            text = text + " ".join(extracted_txt)
        return text

    def search(self, institutions, faculties, lecturer, course, year, freetext):
        """Perform Search according to given parameters."""
        with sqlite3.connect(self.db_name) as con:
            args = []
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
            if institutions:
                where = (
                    where
                    + """
                AND Institutions.InstitutionName == ?
                """
                )
                args.append(institutions)
            if faculties:
                where = (
                    where
                    + """
                AND Faculties.FacultyName == ?
                """
                )
                args.append(faculties)
            if lecturer:
                where = (
                    where
                    + """
                AND Lecturers.LecturerName == ?
                """
                )
                args.append(lecturer)
            if course:
                where = (
                    where
                    + """
                AND Courses.CourseName == ?
                """
                )
                args.append(course)
            if year:
                where = (
                    where
                    + """
                AND Courses.Year == ?
                """
                )
                args.append(year)
            cur = con.execute(select + from_ + where, args)
            result = cur.fetchall()
            if freetext:
                relevant_file_ids = []
                for res in result:
                    relevant_file_ids.append(res[5])
                document_ids = self.free_text_engine.search_free_text(
                    freetext, relevant_file_ids
                )
                result = [t for id_ in document_ids for t in result if str(t[5]) == id_]
            return {"files": result}
