import re
from cryptography.fernet import Fernet

# Secret key for passwords
sec_key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='

def encryptPassword(password):
    """Function that returns encrypted password"""

    # Encrypt passwords
    cipher_suite = Fernet(sec_key)
    ciphered_text = cipher_suite.encrypt(str(password).encode("utf-8"))

    return (ciphered_text)

def decryptPassword(password):
    """Function that returns decrypted password"""

    # Decrypt password
    cipher_suite = Fernet(sec_key)
    unciphered_text = (cipher_suite.decrypt(password))

    return (unciphered_text.decode('utf-8'))


class User():
    """
    Class for object of user that constructed from username, firstname,
    lastname, password, institutionID, FacultyID, study year, role, isBanned.
    """

    def __init__(self, username, fName, lName, password, institutionID, facultyID, studyYear, isBanned = 0):
        """Ctor function for object of user"""
        self.username = username
        self.fName = fName
        self.lName = lName
        self.password = password
        self.institutionID = institutionID
        self.facultyID = facultyID
        self.studyYear = studyYear
        self.role = 1
        self.isBanned = isBanned

    def getUsername(self):
        """The function retruns username of user"""
        return (self.username)
    
    def getFName(self):
        """The function retruns firstname of user"""
        return (self.fName)
    
    def getLName(self):
        """The function retruns lastname of user"""
        return (self.lName)

    def getPassword(self):
        """The function retruns password of user"""
        return (self.password)

    def getInstitutionID(self):
        """The function retruns institution ID of user"""
        return (self.institutionID)
    
    def getFacultyID(self):
        """The function retruns faculty ID of user"""
        return (self.facultyID)
    
    def getStudyYear(self):
        """The function retruns study year of user"""
        return (self.studyYear)

    def getRole(self):
        """The function retruns role of user"""
        return (self.role)
    
    def getIsBanned(self):
        """The function retruns isBanned flag of user"""
        return (self.isBanned)
    
    def setFName(self, fName):
        """The function sets firstname of user"""
        self.fName = fName

    def setLName(self, lName):
        """The function sets lastname of user"""
        self.lName = lName
    
    def setPassword(self, password):
        """The function sets password of user"""
        self.password = password

    def setInstitutionID(self, institutionID):
        """The function sets institution ID of user"""
        self.institutionID = institutionID
    
    def setFacultyID(self, facultyID):
        """The function sets faculty ID of user"""
        self.facultyID = facultyID

    def setStudyYear(self, studyYear):
        """The function sets study year of user"""
        self.studyYear = studyYear

    def setRole(self, role):
        """The function sets role of user"""
        self.role = role
    
    def setIsBanned(self, isBanned):
        """The function sets isBanned flag of user"""
        self.isBanned = isBanned

    def validateUser(self):
        """Function to validate user data"""
        msg = ""

        # Regular expressions
        regUserName = "^[a-zA-Z0-9]+$"
        regPassword = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

        # Check if username is incorrect
        if (not re.match(regUserName, self.getUsername())):
            msg += "User name was incorrect!\n"

        # Check if firstname is not empty
        if (self.getFName() == ""):
            msg += "First name was not entered!\n"

        # Check if lastname is not empty
        if (self.getLName() == ""):
            msg += "Last name is not entered!\n"

        # Check if password is incorrect
        if (not re.match(regPassword, self.getPassword())):
            msg += "Password must be constructed from minimum eight characters, " +\
                    "at least one uppercase letter, one lowercase letter, " +\
                    "one digit, and one special character!\n"
        
        # Check if no institution selected
        if (self.getInstitutionID() == ""):
            msg += "Institution was not selected!\n"

        # Check if no faculty selected
        if (self.getFacultyID() == ""):
            msg += "Faculty was not selected!\n"

        return (msg)

    def validatePassword(self, password):
        """Function to validate user password at login"""
        return (self.getPassword() == password)