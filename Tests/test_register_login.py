import pytest
from static.classes.User import User

class TestRegister:
    def test_username_letters_only_valid(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validateUser() == ""

    def test_username_numbers_only_valid(self):
        username = "1234"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validateUser() == ""

    def test_username_numbers_and_letters_valid(self):
        username = "Aviel1234"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validateUser() == ""

    def test_username_special_chars_invalid(self):
        username = "Aviel1234_!"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validateUser() != ""

    def test_nonempty_firstname_valid(self):
        firstname = "aviel"
        usr = User("testing", firstname, "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validateUser() == ""

    def test_empty_firstname_invalid(self):
        firstname = ""
        usr = User("testing", firstname, "aaa", "Aa123456!", 1, 1, 1)
        assert usr.validateUser() != ""

    def test_nonempty_lastname_valid(self):
        lastname = "rois"
        usr = User("testing", "aviel", lastname, "Aa123456!", 1, 1, 1)
        assert usr.validateUser() == ""

    def test_empty_lastname_invalid(self):
        lastname = ""
        usr = User("testing", "aviel", lastname, "Aa123456!", 1, 1, 1)
        assert usr.validateUser() != ""

    def test_password_letters_only_invalid(self):
        password = "aaaa"
        usr = User("Aviel", "aaa", "aaa", password, 1, 1, 1)
        assert usr.validateUser() != ""

    def test_password_lower_and_upper_letters_only_invalid(self):
        password = "Aaaaa"
        usr = User("Aviel", "aaa", "aaa", password, 1, 1, 1)
        assert usr.validateUser() != ""
    
    def test_password_lower_upper_digits_short_invalid(self):
        password = "Aaa123"
        usr = User("Aviel", "aaa", "aaa", password, 1, 1, 1)
        assert usr.validateUser() != ""
        
    def test_password_lower_upper_digits_special_short_invalid(self):
        password = "Aaa123!"
        usr = User("Aviel", "aaa", "aaa", password, 1, 1, 1)
        assert usr.validateUser() != ""
    
    def test_password_lower_upper_digits_special_long_valid(self):
        password = "Aa123456!"
        usr = User("Aviel", "aaa", "aaa", password, 1, 1, 1)
        assert usr.validateUser() == ""

    def test_nonempty_institution_valid(self):
        institutionID = 1
        usr = User("testing", "aviel", "rois", "Aa123456!", institutionID, 1, 1)
        assert usr.validateUser() == ""

    def test_empty_institution_invalid(self):
        institutionID = ""
        usr = User("testing", "aviel", "rois", "Aa123456!", institutionID, 1, 1)
        assert usr.validateUser() != ""

    def test_nonempty_faculty_valid(self):
        facultyID = 1
        usr = User("testing", "aviel", "rois", "Aa123456!", 1, facultyID, 1)
        assert usr.validateUser() == ""

    def test_empty_faculty_invalid(self):
        facultyID = ""
        usr = User("testing", "aviel", "rois", "Aa123456!", 1, facultyID, 1)
        assert usr.validateUser() != ""

class TestLogin:
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
    