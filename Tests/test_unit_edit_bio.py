import pytest
from static.classes.User import User

class TestEditBio:
    def test_edit_firstname_valid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setFName("test1")
        assert usr.validateUser() == ""

    def test_edit_firstname_invalid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setFName("")
        assert usr.validateUser() != ""

    def test_edit_lastname_valid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setLName("test1")
        assert usr.validateUser() == ""

    def test_edit_lastname_invalid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setLName("")
        assert usr.validateUser() != ""
    
    def test_edit_email_valid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setEmail("aaa@aaa.com")
        assert usr.validateUser() == ""

    def test_edit_email_empty_valid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setEmail("")
        assert usr.validateUser() == ""

    def test_edit_email_invalid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setEmail("aaaaa")
        assert usr.validateUser() != ""

    def test_edit_password_valid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setPassword("Test123456!")
        assert usr.validateUser() == ""

    def test_edit_password_invalid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usr.setPassword("aaaaa")
        assert usr.validateUser() != ""
  
    
