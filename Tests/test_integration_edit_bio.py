import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
import sqlite3
from static.classes.User import User, encryptPassword, decryptPassword

# Global variable
# Prepare the user and password for test
username_test = "test111"
password_test = "Aa123456!!"
institution_test = "SCE_Test"
faculty_test = "Chemistry_Test"
instID = 0
facID = 0

# Create new institution test
newInstTest = "BGU_Test"

@pytest.fixture
def db_prepare_edit_bio():
    global instID, facID

    # Prepare the institution
    db_name = "database.db"

    # connect to db to prepare it before testing
    con = sqlite3.connect(db_name)
    cursor=con.cursor()

    # Check if institution exists
    sqlQueryCheckExist = "SELECT * FROM Institutions WHERE InstitutionName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (institution_test,))
    record = sqlRes.fetchone()
    
    # If institution does not exists create it
    if record == None:
        sqtInsertInst = "INSERT INTO Institutions (InstitutionName) VALUES (?)"
        cursor.execute(sqtInsertInst, (institution_test,))
        instID = cursor.lastrowid
    else:
        instID = record[0]
    
    # Check if faculty exists
    sqlQueryCheckExist = "SELECT * FROM Faculties WHERE FacultyName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (faculty_test,))
    record = sqlRes.fetchone()
    
    # If faculty does not exists create it
    if record == None:
        sqlInsertFac = "INSERT INTO Faculties (FacultyName) VALUES (?)"
        cursor.execute(sqlInsertFac, (faculty_test,))
        facID = cursor.lastrowid
    else:
        facID = record[0]

    # Check if institution and faculty exists in FacIn table
    sqlQueryCheckExist = "SELECT * FROM FacIn WHERE InstitutionID = (?) AND FacultyID = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (instID, facID))
    record = sqlRes.fetchone()
    
    # If institution and faculty does not exists create it
    if record == None:
        sqtInsertInstFac = "INSERT INTO FacIn VALUES (?, ?)"
        con.execute(sqtInsertInstFac, (instID, facID))

    # Check if user exists in Users table
    sqlQueryCheckExist = "SELECT * FROM Users WHERE UserName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (username_test,))
    record = sqlRes.fetchone()
    
    # If user does not exists create it
    if record == None:
        sqtInsertUser = "INSERT INTO Users VALUES (?,?, ?, ?, ?, ?, ?, 1, 0, ?)"
        con.execute(sqtInsertUser, (username_test, "test1", "test1", encryptPassword(password_test), instID, facID, 2, ""))
    
    # Commit the changes in users table
    con.commit()

    #----------------------------------------------------------------
    yield db_name

    # Check if user exists
    sqlQueryCheckExist = "SELECT * FROM Users WHERE UserName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (username_test,))
    record = sqlRes.fetchone()
    
    # If user exists delete the user from DB
    if record != None:
        sqlDelete = "DELETE FROM Users WHERE UserName = (?)"
        sqlRes = con.execute(sqlDelete, (username_test,))

    # Check if institution and faculty exists in FacIn table
    sqlQueryCheckExist = "SELECT * FROM FacIn WHERE InstitutionID = (?) AND FacultyID = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (instID, facID))
    record = sqlRes.fetchone()
    
    # If faculty in institution exists delete it
    if record != None:
        sqtDelInstFac = "DELETE FROM FacIn WHERE InstitutionID = (?) AND FacultyID = (?)"
        con.execute(sqtDelInstFac, (instID, facID))

    # Check if institution and faculty exists in FacIn table
    sqlQueryCheckExist = "SELECT * FROM FacIn WHERE InstitutionID = (SELECT InstitutionID FROM Institutions WHERE InstitutionName = (?)) AND FacultyID = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (newInstTest, facID))
    record = sqlRes.fetchone()

    # If faculty in institution exists delete it
    if record != None:
        sqtDelInstFac = "DELETE FROM FacIn WHERE InstitutionID = (?) AND FacultyID = (?)"
        con.execute(sqtDelInstFac, (record[0], facID))

    # Check if faculty exists
    sqlQueryCheckExist = "SELECT * FROM Faculties WHERE FacultyName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (faculty_test,))
    record = sqlRes.fetchone()
    
    # If faculty exists delete it
    if record != None:
        sqlDelFac = "DELETE FROM Faculties WHERE FacultyID = (?)"
        con.execute(sqlDelFac, (facID,))

    # Check if institution exists
    sqlQueryCheckExist = "SELECT * FROM Institutions WHERE InstitutionName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (institution_test,))
    record = sqlRes.fetchone()
    
    # If institution exists create it
    if record != None:
        sqtDelInst = "DELETE FROM Institutions WHERE InstitutionID = (?)"
        con.execute(sqtDelInst, (instID,))

    # Check if additional institution exists
    sqlQueryCheckExist = "SELECT * FROM Institutions WHERE InstitutionName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (newInstTest,))
    record = sqlRes.fetchone()
    
    # If institution exists create it
    if record != None:
        sqtDelInst = "DELETE FROM Institutions WHERE InstitutionID = (?)"
        con.execute(sqtDelInst, (record[0],))

    # Commit the changes in users table
    con.commit()

    # CLose connection to DB
    con.close()

class TestEditBio:
    def test_user_info_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_edit_bio):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the login page
        ff_browser.get(application + "/login")

        # Get username and password elements on page
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")

        # Get submit button element
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject username and password of test user
        username.send_keys(username_test)
        password.send_keys(password_test)

        # Click on submit button
        btnSubmit.click()

        # Open the control panel page
        ff_browser.get(application + "/user/" + username_test)

        # Get header Object
        profHeader = ff_browser.find_element_by_name("profileHeader")

        assert (profHeader.text == username_test + "'s profile")
    
    def test_user_info_of_other_user_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_edit_bio):
        # Run logout to clean session
        ff_browser.get(application + "/logout")

        # Open the control panel page
        ff_browser.get(application + "/user/" + username_test)

        # Get header Object
        profHeader = ff_browser.find_element_by_name("profileHeader")

        assert (profHeader.text == username_test + "'s profile")

    def test_edit_bio_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_edit_bio):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the login page
        ff_browser.get(application + "/login")

        # Get username and password elements on page
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")

        # Get submit button element
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject username and password of test user
        username.send_keys(username_test)
        password.send_keys(password_test)

        # Click on submit button
        btnSubmit.click()
        
        # Open the control panel page
        ff_browser.get(application + "/user/" + username_test)

        # Get header Object
        btnEditBio = ff_browser.find_element_by_xpath("/html/body/div[2]/div[2]/a[1]/button")

        # Click button
        btnEditBio.click()

        # Get the header in edit bio page
        editBioHeader = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (editBioHeader.text == "Change bio of " + username_test + "'s user")

    def test_change_pass_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_edit_bio):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the login page
        ff_browser.get(application + "/login")

        # Get username and password elements on page
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")

        # Get submit button element
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject username and password of test user
        username.send_keys(username_test)
        password.send_keys(password_test)

        # Click on submit button
        btnSubmit.click()
        
        # Open the control panel page
        ff_browser.get(application + "/user/" + username_test)

        # Get header Object
        btnChangePass = ff_browser.find_element_by_xpath("/html/body/div[2]/div[2]/a[2]/button")

        # Click button
        btnChangePass.click()

        # Get the header in edit bio page
        changePassHeader = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (changePassHeader.text == "Change password of " + username_test)

    def test_change_pass_of_user(self, application: str, ff_browser: webdriver.Firefox, db_prepare_edit_bio):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the login page
        ff_browser.get(application + "/login")

        # Get username and password elements on page
        username = ff_browser.find_element_by_name("username")
        password = ff_browser.find_element_by_name("password")

        # Get submit button element
        btnSubmit = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject username and password of test user
        username.send_keys(username_test)
        password.send_keys(password_test)

        # Click on submit button
        btnSubmit.click()
        
        # Open the control panel page
        ff_browser.get(application + "/user/" + username_test)

        # Get header Object
        btnChangePass = ff_browser.find_element_by_xpath("/html/body/div[2]/div[2]/a[2]/button")

        # Click button
        btnChangePass.click()

        # Send password
        password = ff_browser.find_element_by_name("password")
        passwordConfirm = ff_browser.find_element_by_name("confirmPass")

        # Get submit button element
        btnSave = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Inject password and confirm
        password.send_keys(password_test + "!")
        passwordConfirm.send_keys(password_test + "!")

        # Click save buttoon
        btnSave.click()

        # Get header Object
        profHeader = ff_browser.find_element_by_name("profileHeader")

        assert (profHeader.text == username_test + "'s profile")