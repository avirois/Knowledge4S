import pytest
from static.classes.User import User

class TestFile:
    def test_password_login_valid(self):
        username = "t1"
        password = "Aa123456!"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validatePassword(password)

    def test_password_login_invalid(self):
        username = "t1"
        password = "Aa123"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert not usr.validatePassword(password)

    def test_banned_user(self):
        username = "t1"
        password = "Aa123"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1, 1)
        assert (usr.getIsBanned() == 1)
