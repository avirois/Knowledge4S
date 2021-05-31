import pytest

from blueprints.manageLecturers import (
    checkAddInput,
    checkRemoveInput,
    add_lecturer_to_db,
    remove_lecturer_from_db,
)


class TestUnitManageLEcturers:
    def test_checkRemoveInput_wrong_name(self, fill_db):
        assert checkRemoveInput("932341", "A", "math") is False

    def test_checkRemoveInput_worng_institution(self, fill_db):
        assert checkRemoveInput("Moshe", "Aasdasd", "math") is False

    def test_checkRemoveInput_worng_faculty(self, fill_db):
        assert checkRemoveInput("Moshe", "Aasdasd", "math") is False

    def test_checkRemoveInput_correct(self, fill_db):
        assert checkRemoveInput("Moshe", "A", "math")

    def test_checkRemoveInput_empty_db(self):
        assert checkRemoveInput("Moshe", "A", "math") is False

    def test_checkAddInput_empty_db(self):
        assert checkAddInput("Moshe", "A", "math") is False

    def test_checkAddInput_bad_name(self, fill_db):
        assert checkAddInput("Moshe123", "A", "math") is False

    def test_checkAddInput_name(self, fill_db):
        assert checkAddInput("Yosi", "A", "math")

    def test_checkAddInput_name_surname(self, fill_db):
        assert checkAddInput("Yosi Yosef", "A", "math")

    def test_checkAddInput_wrong_faculty(self, fill_db):
        assert checkAddInput("Yosi Yosef", "A", "mathasdasd") is False

    def test_checkAddInput_wrong_institution(self, fill_db):
        assert checkAddInput("Yosi Yosef", "Aasdasd", "math") is False

    def test_remove_lecturer_from_db(self, fill_db):
        remove_lecturer_from_db("Moshe", "A", "math")
        assert checkAddInput("Moshe", "A", "math")

    def test_add_add_lecturer_to_db(self, fill_db):
        add_lecturer_to_db("Yosi", "A", "math")
        assert checkRemoveInput("Yosi", "A", "math")
