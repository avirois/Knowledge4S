from static.classes.User import User

class Admin(User):
    """
    Class for object of admin that constructed from username, firstname,
    lastname, password, institutionID, FacultyID, study year, role, isBanned.
    """

    def __init__(self, username, fName, lName, password, institutionID, facultyID, studyYear, isBanned = 0, email = None):
        """Ctor function for object of Admin"""
        super().__init__(username, fName, lName, password, institutionID, facultyID, studyYear, isBanned, email)
        self.role = 1

    def isAdmin(self):
        """ The function returns true if current user is admin """
        return (True)