import pytest
from static.classes.User import User

class TestUserFile:
    def test_show_list_files(self):
        username = "t1"
        password = "Aa123456!"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validatePassword(password)

    def test_show_pending_file(self):
        username = "t1"
        password = "Aa123"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert not usr.validatePassword(password)

    def test_show_approved_files(self):
        username = "t1"
        password = "Aa123"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1, 1)
        assert (usr.getIsBanned() == 1)
