import pytest
from static.classes.User import User
from static.classes.Admin import Admin

class TestManageUsers:
    def test_ban_user(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1, 1)

        assert usr.getIsBanned() == 1
    
    def test_unban_user(self):
        username = "Aviel"
        usr = User(username, "aaa", "aaa", "Aa123456!", 1, 1, 1, 0)

        assert usr.getIsBanned() == 0

    def test_grant_admin(self):
        username = "Aviel"
        usr = Admin(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        
        assert usr.isAdmin() == True
    
    def test_revoke_admin(self):
        username = "Aviel"
        usrAdmin = Admin(username, "aaa", "aaa", "Aa123456!", 1, 1, 1)
        usrAdmin.__class__ = User
        
        assert usrAdmin.isAdmin() == False

    