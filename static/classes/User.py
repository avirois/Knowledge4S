import re
import sqlite3
from cryptography.fernet import Fernet
from static.classes.Institution import Institution
from static.classes.Faculty import Faculty
from flask import current_app

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

    def __init__(self, username, fName, lName, password, institutionID, facultyID, studyYear, isBanned = 0, email = None):
        """Ctor function for object of user"""
        self.username = username
        self.fName = fName
        self.lName = lName
        self.email = email
        self.password = password
        self.institutionID = institutionID
        self.facultyID = facultyID
        self.studyYear = studyYear
        self.role = 0
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

    def getEmail(self):
        """The function retruns email of user"""
        return (self.email)

    def getPassword(self):
        """The function retruns password of user"""
        return (self.password)

    def getInstitutionID(self):
        """The function retruns institution ID of user"""
        return (self.institutionID)

    def getInstitutionName(self):
        """The function retruns the name of the institution of the user"""
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryLogin = "SELECT * FROM Institutions WHERE InstitutionID = (?)"

        # Run the query to get institution data
        sqlRes = con.execute(sqlQuryLogin,(self.getInstitutionID(),))

        # Fetch the result
        record = sqlRes.fetchone()

        # Create institution object for current selected username
        instOfUser = None

        # Check if user exists
        if (record != None):
            # Create institution object for current selected username
            instOfUser = Institution(record[0], record[1])

        # Close the connection to the database
        con.close()

        return (instOfUser.getName())
    
    def getFacultyID(self):
        """The function retruns faculty ID of user"""
        return (self.facultyID)

    def getFacultyName(self):
        """The function retruns the name of the faculty of the user"""
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryLogin = "SELECT * FROM Faculties WHERE FacultyID = (?)"

        # Run the query to get faculty data
        sqlRes = con.execute(sqlQuryLogin,(self.getFacultyID(),))

        # Fetch the result
        record = sqlRes.fetchone()

        # Create facullty object for current selected username
        facOfUser = None

        # Check if user exists
        if (record != None):
            # Create faculty object for current selected username
            facOfUser = Faculty(record[0], record[1])

        # Close the connection to the database
        con.close()

        return (facOfUser.getName())
    
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
    
    def setEmail(self, email):
        """The function sets email of user"""
        self.email = email
    
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
        regEmail = "\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+"

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

        # Check if email entered
        if ((self.getEmail() != None) and (self.getEmail() != "")):
            # Check if email is correct
            if (not re.match(regEmail, self.getEmail())):
                msg += "Email is incorrect!\n"

        return (msg)

    def validateEditBio(self):
        """Function to validate user data at edit bio"""
        msg = ""

        # Regular expressions
        regEmail = "\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+"

        # Check if firstname is not empty
        if (self.getFName() == ""):
            msg += "First name was not entered!\n"

        # Check if lastname is not empty
        if (self.getLName() == ""):
            msg += "Last name is not entered!\n"

        # Check if no institution selected
        if (self.getInstitutionID() == ""):
            msg += "Institution was not selected!\n"

        # Check if no faculty selected
        if (self.getFacultyID() == ""):
            msg += "Faculty was not selected!\n"

        # Check if email entered
        if ((self.getEmail() != None) and (self.getEmail() != "")):
            # Check if email is correct
            if (not re.match(regEmail, self.getEmail())):
                msg += "Email is incorrect!\n"

        return (msg)

    def validatePassword(self, password):
        """Function to validate user password at login"""
        return (self.getPassword() == password)

    def isAdmin(self):
        """ The function returns false if user is not admin """
        return (False)