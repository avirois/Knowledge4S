import pytest
from blueprints.update import is_uer_own_file


class TestUnitUpdate:
    def test_is_uer_own_file(
        self,
        fill_db,
    ):
        assert is_uer_own_file(1, "sskdfjsk", "database.db") == False
        assert is_uer_own_file(2, "Moshe", "database.db") == True
