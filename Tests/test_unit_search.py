import json
import os
import pytest
import sqlite3
from modules.selection import Selections
import modules.search as sm
import modules.search_by_free_text as sft
import modules.search_by_sql_queries as ssq

DB_NAME = "database.db"
TEST_STORAGE_1 = "Tests/test_storage_1"


@pytest.fixture
def use_test_storage1():
    sft.STORAGE = TEST_STORAGE_1


#  ____                      _       _                       _
# / ___|  ___  __ _ _ __ ___| |__   | |__  _   _   ___  __ _| |
# \___ \ / _ \/ _` | '__/ __| '_ \  | '_ \| | | | / __|/ _` | |
#  ___) |  __/ (_| | | | (__| | | | | |_) | |_| | \__ \ (_| | |
# |____/ \___|\__,_|_|  \___|_| |_| |_.__/ \__, | |___/\__, |_|
#                                          |___/          |_|
#              _ _     _            _
#  _   _ _ __ (_) |_  | |_ ___  ___| |_ ___
# | | | | '_ \| | __| | __/ _ \/ __| __/ __|
# | |_| | | | | | |_  | ||  __/\__ \ |_\__ \
#  \__,_|_| |_|_|\__|  \__\___||___/\__|___/


class TestSearchBySql:
    def test_can_search_with_empty_db(self):
        a = ssq.search_by_sql_queries(DB_NAME, "A", "math", "all", "all", "all")
        b = ssq.search_by_sql_queries(DB_NAME, "", "", "", "", "all")
        assert isinstance(a, list)
        assert isinstance(b, list)

    def test_can_search_with_db(self, fill_db):
        a = ssq.search_by_sql_queries(DB_NAME, "all", "all", "all", "all", "all")
        assert len(a) > 0

    def test_bad_input(self, fill_db):
        res = []
        options = ("all", "", None)
        for opt0 in options[1:]:
            for opt1 in options:
                for opt2 in options:
                    for opt3 in options:
                        for opt4 in options:
                            res.append(ssq.search_by_sql_queries(
                                DB_NAME, opt0, opt1, opt2, opt3, opt4
                            ))
        assert len([j for i in res for j in i]) == 0

    def test_can_find_math_course(self, fill_db):
        excepted = [('Calculus',
                '1.1.2021',
                '1.1.2021',
                'special number',
                'math',
                1,
                'F1.txt',
                'A',
                'title-math',
                'Yosi'),]
        for opt0 in ("all", "A"):
            for opt1 in ("all", "math"):
                for opt2 in ("all", "Moshe"):
                    for opt3 in ("all", "Calculus"):
                        for opt4 in ("all", "2021"):
                            if (opt0 != "all" or opt1 != "all" or
                                opt2 != "all" or opt3 != "all"):
                                assert excepted == ssq.search_by_sql_queries(
                                    DB_NAME, opt0, opt1, opt2, opt3, opt4
                                )

    def test_can_find_art_course(self, fill_db):
        excepted = [('study of drawing',
                                    '1.1.2021',
                                    '1.1.2021',
                                    'sokal-affair',
                                    'art',
                                    2,
                                    'F2.txt',
                                    'B',
                                    'titile-sokal',
                                    'Moshe'),
                                  ]
        for opt0 in ("all", "B"):
            for opt1 in ("all", "art"):
                for opt2 in ("all", "Sarah"):
                    for opt3 in ("all", "study of drawing"):
                        for opt4 in ("all", "2021"):
                            if (opt0 != "all" or opt1 != "all" or
                                opt2 != "all" or opt3 != "all"):
                                assert excepted == ssq.search_by_sql_queries(
                                    DB_NAME, opt0, opt1, opt2, opt3, opt4
                                )


#  ____                      _       _              __
# / ___|  ___  __ _ _ __ ___| |__   | |__  _   _   / _|_ __ ___  ___
# \___ \ / _ \/ _` | '__/ __| '_ \  | '_ \| | | | | |_| '__/ _ \/ _ \
#  ___) |  __/ (_| | | | (__| | | | | |_) | |_| | |  _| | |  __/  __/
# |____/ \___|\__,_|_|  \___|_| |_| |_.__/ \__, | |_| |_|  \___|\___|
#                                          |___/
#  _            _                 _ _     _            _
# | |_ _____  _| |_   _   _ _ __ (_) |_  | |_ ___  ___| |_
# | __/ _ \ \/ / __| | | | | '_ \| | __| | __/ _ \/ __| __|
# | ||  __/>  <| |_  | |_| | | | | | |_  | ||  __/\__ \ |_
#  \__\___/_/\_\\__|  \__,_|_| |_|_|\__|  \__\___||___/\__|


class TestSearchByFreeText:

    def test_can_search_existing_text(self,use_test_storage1):
        res = sft.oreder_by__containing_freetext("number",[1,2])
        assert res == ["1", "2"]
        res = sft.oreder_by__containing_freetext("sokal",[1,2])
        assert res == ["2", "1"]
    
    def test_can_search_by_non_existing_text(self,use_test_storage1):
        res = sft.oreder_by__containing_freetext("oogabooga",[1,2])
        assert res == ["1", "2"]
        res = sft.oreder_by__containing_freetext("cake",[1,2])
        assert res == ["1", "2"]
    


#  ____                      _                   _ _     _            _
# / ___|  ___  __ _ _ __ ___| |__    _   _ _ __ (_) |_  | |_ ___  ___| |_
# \___ \ / _ \/ _` | '__/ __| '_ \  | | | | '_ \| | __| | __/ _ \/ __| __|
#  ___) |  __/ (_| | | | (__| | | | | |_| | | | | | |_  | ||  __/\__ \ |_
# |____/ \___|\__,_|_|  \___|_| |_|  \__,_|_| |_|_|\__|  \__\___||___/\__|
#

class TestSearch:

    def test_can_search_with_empty_db(self):
        res = sm.search("database.db", "all", "all", "all", "all", "1984" , "2+2=5")
        assert res ==[]

    def test_can_search_with_db(self, fill_db):
        res = sm.search("database.db", "A", "math", "all", "all", "2021" , "number")
        assert res ==[('Calculus', '1.1.2021',  '1.1.2021',  'special number',  'math',  1,  'F1.txt',  'A',  'title-math',  'Yosi')]

#  ____       _           _   _                               _ _
# / ___|  ___| | ___  ___| |_(_) ___  _ __  ___   _   _ _ __ (_) |_
# \___ \ / _ \ |/ _ \/ __| __| |/ _ \| '_ \/ __| | | | | '_ \| | __|
#  ___) |  __/ |  __/ (__| |_| | (_) | | | \__ \ | |_| | | | | | |_
# |____/ \___|_|\___|\___|\__|_|\___/|_| |_|___/  \__,_|_| |_|_|\__|
#
#  _            _
# | |_ ___  ___| |_
# | __/ _ \/ __| __|
# | ||  __/\__ \ |_
#  \__\___||___/\__|


class TestSelection:
    def test_can_create_selection_with_empty_db(self):
        selections = Selections(DB_NAME)
        assert isinstance(selections, Selections)

    def test_error_when_bad_db(self):
        try:
            Selections("im_not_db.db")
            os.remove("im_not_db.db")
            assert False
        except sqlite3.OperationalError:
            os.remove("im_not_db.db")
            assert True

    def test_work_on_empty_db(self):
        selections = Selections(DB_NAME).get_selections(
            faculties="all",
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

    def test_get_selection_work_with_non_existing_facultie(self):
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

    def test_get_selection_work_with_non_existing_year(self):
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

    def test_get_selections_with_no_args(self):
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

    def test_get_selections_with_some_args(self):
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

    def test_get_selections_year_can_be_str(self):
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

    def test_can_create_selection_with_db(self, fill_db):
        selections = Selections(DB_NAME)
        assert isinstance(selections, Selections)

    def test_all_selections(self, fill_db):
        selections = Selections(DB_NAME).get_selections(
            institutions="all",
            faculties="all",
            lecturers="all",
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

    def test_selectoin_with_year(self, fill_db):
        selections = Selections(DB_NAME).get_selections(
            institutions="all",
            faculties="all",
            lecturers="all",
            courses="all",
            years=1984,
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

    def test_selectoin_with_institutions(self, fill_db):
        selections = Selections(DB_NAME).get_selections(
            institutions="A",
            faculties="all",
            lecturers="all",
            courses="all",
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

    def test_selectoin_with_faculties(self, fill_db):
        selections = Selections(DB_NAME).get_selections(
            institutions="A",
            faculties="math",
            lecturers="all",
            courses="all",
            years="all",
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

    def test_selectoin_with_lecturer(self, fill_db):
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

    def test_selectoin_with_all_filled(self, fill_db):
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

    def test_selectoin_with_bad_input_1(self, fill_db):
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

    def test_selectoin_with_bad_input_2(self, fill_db):
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

    def test_selectoin_with_bad_input_3(self, fill_db):
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

    def test_selectoin_with_bad_input_4(self, fill_db):
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

    def test_selectoin_with_bad_input_4(self, fill_db):
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

    def test_selectoin_back_deselection(self, fill_db):
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

    def test_should_pass_with_sarah_too(self, fill_db):
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

    def test_select_other_top(self, fill_db):
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

    def test_select_other_top_with_year(self, fill_db):
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

    def test_test_all_combinations(fill_db):
        selections = Selections(DB_NAME)

        institutions = ["A", "B", "all", None]
        faculties = ["math", "art", None]
        lecturers = ["Moshe", "Sarah", None]
        courses = ["Calculus", "study of drawing", None]
        years = ["2021", 2021, None]

        for ins in institutions:
            for fac in faculties:
                for lec in lecturers:
                    for cur in courses:
                        for yer in years:
                            selections.get_selections(
                                institutions=ins,
                                faculties=fac,
                                lecturers=lec,
                                courses=cur,
                                years=yer,
                            )
        assert True
