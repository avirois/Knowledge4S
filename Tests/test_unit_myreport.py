import pytest
from blueprints.report_status import get_my_report


class TestUnitMyReport:
    def test_report_is_list_of_dicts_on_empty_db(
        self,
    ):
        assert type(get_my_report("database.db", "yosi")) == list
