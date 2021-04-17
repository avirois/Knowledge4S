import pytest
from static.classes.Admin import Admin

class TestAdminsInfo:
    def test_admin_valid(self):
        username = "Aviel"
        usr = Admin(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        
        assert usr.validateUser() == ""
    
    def test_admin_invalid(self):
        username = "Aviel"
        usr = Admin(username, "aaa", "aaa", "", 1, 1, 1)
        
        assert usr.validateUser() != ""

    