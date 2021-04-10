import json
import os
import pytest
import sqlite3
from modules.selection import Selections
from modules.util import Singleton
import modules.search as sm
import modules.search_by_free_text as sft
import modules.search_by_sql_queries as ssq

DB_NAME = "database.db"
TEST_STORAGE_1 = "Tests/test_storage_1"
TEST_STORAGE_2 = "Tests/test_storage_2"


@pytest.fixture
def use_test_storage1():
    sm.STORAGE_FOLDER = TEST_STORAGE_1


@pytest.fixture
def use_test_storage2():
    sm.STORAGE_FOLDER = TEST_STORAGE_2




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
    def test_work_on_empty_TFs(self, reset_singletons):
        assert ('1','2','3','4') == sft.DocumentsTermsFrequency().order_by_similarity_to("fat cat", 1, 2, 3, 4)
    
    def test_singeltons(self, reset_singletons):
        a = sft.DocumentsTermsFrequency()
        b = sft.DocumentsTermsFrequency()
        c = sft.DocumentsTermsFrequency()
        a.add_document(1,"hello im fat cat")
        assert a is b
        assert b is c
        assert isinstance(b.word_to_index["cat"] ,int)

    def test_can_add_documents(self, reset_singletons):
        sft.DocumentsTermsFrequency().add_document(1, "hello im fat cat")
        sft.DocumentsTermsFrequency().add_document(2, "woof woof im dog")
        assert isinstance(sft.DocumentsTermsFrequency().documents_term_frequency['1'],list )
        assert isinstance(sft.DocumentsTermsFrequency().documents_term_frequency['2'],list )

    def test_can_recive_relevant_order(self, reset_singletons):
        sft.DocumentsTermsFrequency().add_document(1, "hello im fat fat cat")
        sft.DocumentsTermsFrequency().add_document(2, "woof woof im dog")
        sft.DocumentsTermsFrequency().add_document(3, "fat food")
        assert ('1', '3', '2') == sft.DocumentsTermsFrequency().order_by_similarity_to("the fat i want", 1,2,3)

    


#  ____                      _                   _ _     _            _
# / ___|  ___  __ _ _ __ ___| |__    _   _ _ __ (_) |_  | |_ ___  ___| |_
# \___ \ / _ \/ _` | '__/ __| '_ \  | | | | '_ \| | __| | __/ _ \/ __| __|
#  ___) |  __/ (_| | | | (__| | | | | |_| | | | | | |_  | ||  __/\__ \ |_
# |____/ \___|\__,_|_|  \___|_| |_|  \__,_|_| |_|_|\__|  \__\___||___/\__|
#
text1 = """special number F1.txt title-math Yosi In mathematics, 0.999... (also written as 0.9, in repeating decimal notation) denotes the repeating decimal consisting of an unending sequence of 9s after the decimal point. This repeating decimal represents the smallest number no less than every decimal number in the sequence (0.9, 0.99, 0.999, ...).[1] This number is equal to 1. In other words, "0.999..." and "1" represent the same number. There are many ways of showing this equality, from intuitive arguments to mathematically rigorous proofs. The technique used depends on the target audience, background assumptions, historical context, and preferred development of the real numbers, the system within which 0.999... is commonly defined. (In other systems, 0.999... can have the same meaning, a different definition, or be undefined.) More generally, every nonzero terminating decimal has two equal representations (for example, 8.32 and 8.  31999...), which is a property of all base representations. The utilitarian preference for the terminating decimal representation contributes to the misconception that it is the only representation. For this and other reasons— such as rigorous proofs relying on non-elementary techniques, properties, or disciplines—some people can find the equality sufficiently counterintuitive that they question or reject it. This has been the subject of several studies in mathematics education.""" 
text2 = """sokal-affair F2.txt titile-sokal Moshe The Sokal affair, also called the Sokal hoax,[1] was a demonstrative  scholarly hoax performed by Alan Sokal, a physics professor at New York  University and University College London. In 1996, Sokal submitted an article  to Social Text, an academic journal of postmodern cultural studies. The  submission was an experiment to test the journal's intellectual rigor, and  specifically to investigate whether "a leading North American journal of  cultural studies—whose editorial collective includes such luminaries as  Fredric Jameson and Andrew Ross—[would] publish an article liberally salted  with nonsense if (a) it sounded good and (b) it flattered the editors'  ideological preconceptions The article, "Transgressing the Boundaries: Towards a Transformative  Hermeneutics of Quantum Gravity",[3] was published in the journal's spring/ summer 1996 "Science Wars" issue. It proposed that quantum gravity is a  social and linguistic construct. At that time, the journal did not practice  academic peer review and it did not submit the article for outside expert  review by a physicist.[4][5] Three weeks after its publication in May 1996,  Sokal revealed in the magazine Lingua Franca that the article was a hoax The hoax caused controversy about the scholarly merit of commentary on the  physical sciences by those in the humanities; the influence of postmodern  philosophy on social disciplines in general; academic ethics, including  whether Sokal was wrong to deceive the editors and readers of Social Text;  and whether Social Text had exercised appropriate intellectual rigor. """


class TestSearch:
    def test_extract_text_from_txt_document(self, use_test_storage1, fill_db):
        assert len(text1.split(" ")) == len(sm.extract_text_from_document(DB_NAME, 1).split(" "))
        assert len(text2.split(" ")) == len(sm.extract_text_from_document(DB_NAME, 2).split(" "))

    def test_extract_text_from_pdf_document(self, use_test_storage2, fill_db):
        assert len(text1.split(" ")) == len(sm.extract_text_from_document(DB_NAME, 1).split(" "))
        assert len(text2.split(" ")) == len(sm.extract_text_from_document(DB_NAME, 2).split(" "))

    def test_init_search_without_db(self, reset_singletons):
        TFs = sm.init_search(DB_NAME)
        assert isinstance(TFs, sft.DocumentsTermsFrequency)

    def test_init_search_with_db(self, fill_db, reset_singletons, use_test_storage1):
        TFs = sm.init_search(DB_NAME)
        assert len(TFs.documents_term_frequency) == 2
        
    # def test_add_document(self):
    #     pass
    #     
    # def test_order_by_similarity_to(self):
    #     pass
    #
    # def test_search(self):
    #     pass


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
