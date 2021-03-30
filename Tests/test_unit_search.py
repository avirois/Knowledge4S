import sqlite3
import pytest
import os
from modules.selection import Selections
import json

DB_NAME = "database.db"


@pytest.fixture
def fill_db():
    with sqlite3.connect(DB_NAME) as con:
        # setup
        con.execute("DELETE FROM Faculties")
        con.execute("DELETE FROM Institutions")
        con.execute("DELETE FROM Lecturers")
        con.execute("DELETE FROM Courses")
        con.execute("DELETE FROM FacIn")
        # 1)
        con.execute("INSERT INTO Institutions VALUES (?, ?)", (1, "A"))
        con.execute("INSERT INTO Faculties VALUES (?, ?)", (11, "math"))

        con.execute("INSERT INTO Lecturers VALUES (?, ?, ?, ?)", (1111, "Moshe", 11, 1))
        con.execute(
            "INSERT INTO Courses VALUES (?, ?, ?, ?)", (111, "Calculus", 1111, 2021)
        )
        con.execute("INSERT INTO FacIn VALUES (?, ?)", (1, 11))
        # 2)
        con.execute("INSERT INTO Faculties VALUES (?, ?)", (22, "art"))
        con.execute("INSERT INTO Institutions VALUES (?, ?)", (2, "B"))
        con.execute("INSERT INTO Lecturers VALUES (?, ?, ?, ?)", (2222, "Sarah", 22, 2))
        con.execute(
            "INSERT INTO Courses VALUES (?, ?, ?, ?)",
            (222, "study of drawing", 2222, 2021),
        )
        con.execute("INSERT INTO FacIn VALUES (?, ?)", (2, 22))
    yield
    # Teardown :
    with sqlite3.connect(DB_NAME) as con:
        con.execute("DELETE FROM Faculties")
        con.execute("DELETE FROM Institutions")
        con.execute("DELETE FROM Lecturers")
        con.execute("DELETE FROM Courses")
        con.execute("DELETE FROM FacIn")


def test_can_create_selection_with_empty_db():
    selections = Selections(DB_NAME)
    assert isinstance(selections, Selections)


def test_error_when_bad_db():
    try:
        Selections("im_not_db.db")
        os.remove("im_not_db.db")
        assert False
    except sqlite3.OperationalError:
        os.remove("im_not_db.db")
        assert True


def test_work_on_empty_db():
    selections = Selections(DB_NAME).get_selections(
        faculties="all", institutions="all", lecturers="all", courses="all", years="all"
    )

    expected = {
        "faculties": tuple(),
        "institutions": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": tuple(),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_get_selection_work_with_non_existing_facultie():
    selections = Selections(DB_NAME).get_selections(
        faculties="math",
        institutions="all",
        lecturers="all",
        courses="all",
        years="all",
    )

    expected = {
        "faculties": tuple(),
        "institutions": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": tuple(),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_get_selection_work_with_non_existing_year():
    selections = Selections(DB_NAME).get_selections(
        faculties="all",
        institutions="all",
        lecturers="all",
        courses="all",
        years=1984,
    )

    expected = {
        "faculties": tuple(),
        "institutions": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": tuple(),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_get_selections_with_no_args():
    selections = Selections(DB_NAME).get_selections()

    expected = {
        "faculties": tuple(),
        "institutions": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": tuple(),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_get_selections_with_some_args():
    selections = Selections(DB_NAME).get_selections(years=1984)

    expected = {
        "faculties": tuple(),
        "institutions": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": tuple(),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_get_selections_year_can_be_str():
    selections = Selections(DB_NAME).get_selections(years="1984")

    expected = {
        "faculties": tuple(),
        "institutions": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": tuple(),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_can_create_selection_with_db(fill_db):
    selections = Selections(DB_NAME)
    assert isinstance(selections, Selections)


def test_all_selections(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="all", faculties="all", lecturers="all", courses="all", years="all"
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_year(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="all", faculties="all", lecturers="all", courses="all", years=1984
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_institutions(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A", faculties="all", lecturers="all", courses="all", years="all"
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_faculties(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A", faculties="math", lecturers="all", courses="all", years="all"
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": ("Moshe",),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_lecturer(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="math",
        lecturers="Moshe",
        courses="all",
        years="all",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": ("Moshe",),
        "courses": ("Calculus",),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_all_filled(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="math",
        lecturers="Moshe",
        courses="Calculus",
        years=2021,
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": ("Moshe",),
        "courses": ("Calculus",),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_bad_input_1(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="all",
        faculties="all",
        lecturers="all",
        courses="Calculus",
        years="all",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_bad_input_2(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="all",
        faculties="all",
        lecturers="kukurikoooooooo",
        courses="all",
        years="all",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_bad_input_3(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="something",
        faculties="all",
        lecturers="kukurikoooooooo",
        courses="all",
        years="all",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": tuple(),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_bad_input_4(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="lets try",
        lecturers="make",
        courses="it",
        years="fail",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_with_bad_input_4(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="math",
        lecturers="will",
        courses="it",
        years="fail?",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": ("Moshe",),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_selectoin_back_deselection(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="all",
        lecturers="Moshe",
        courses="all",
        years="2021",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_should_pass_with_sarah_too(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="B",
        faculties="art",
        lecturers="Sarah",
        courses="study of drawing",
        years="2021",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("art",),
        "lecturers": ("Sarah",),
        "courses": ("study of drawing",),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_select_other_top(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="art",
        lecturers="Sarah",
        courses="study of drawing",
        years="all",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str


def test_select_other_top_with_year(fill_db):
    selections = Selections(DB_NAME).get_selections(
        institutions="A",
        faculties="art",
        lecturers="Sarah",
        courses="study of drawing",
        years="2021",
    )

    expected = {
        "institutions": ("A", "B"),
        "faculties": ("math",),
        "lecturers": tuple(),
        "courses": tuple(),
        "years": ("2021",),
    }

    test_dict_str = json.dumps(selections, sort_keys=True)
    except_dict_str = json.dumps(expected, sort_keys=True)

    assert test_dict_str == except_dict_str