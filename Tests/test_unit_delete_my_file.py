import sqlite3
import pytest
from blueprints.delete_my_files import delete_my_file


class TestUnitDelete:
    def test_delete_myfile(
        fill_db,
    ):
        delete_my_file("database.db", 1)
        with sqlite3.connect("database.db") as con:
            res = con.execute("select * from Files where FileID == ?", (1,))
            assert len(res.fetchall()) == 0
