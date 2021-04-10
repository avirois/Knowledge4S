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
newFacTest = "Software_Test"

@pytest.fixture
def db_prepare_manage_fac():
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
        sqtInsertUser = "INSERT INTO Users VALUES (?,?, ?, ?, ?, ?, ?, 1, 0)"
        con.execute(sqtInsertUser, (username_test, "test1", "test1", encryptPassword(password_test), instID, facID, 2))
    
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

    # Check if additional faculty exists
    sqlQueryCheckExist = "SELECT * FROM Faculties WHERE FacultyName = (?)"
    sqlRes = con.execute(sqlQueryCheckExist, (newFacTest,))
    record = sqlRes.fetchone()
    
    # If faculty exists create it
    if record != None:
        sqtDelInst = "DELETE FROM Faculties WHERE FacultyID = (?)"
        con.execute(sqtDelInst, (record[0],))

    # Commit the changes in users table
    con.commit()

    # CLose connection to DB
    con.close()

class TestManageFaculties:
    def test_manage_faculties_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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
        ff_browser.get(application + "/controlpanel")

        # Get manage faculties button
        btnManageFaculties = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/a[2]/button")

        # Click the manage faculties buttons
        btnManageFaculties.click()

        # Get manage faculties title
        manageFacTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (manageFacTitle.text == "Manage Faculties:")
    
    def test_create_faculty_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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
        ff_browser.get(application + "/manage_faculties")

        # Get manage faculty button
        btnCreateFac = ff_browser.find_element_by_xpath("/html/body/div[2]/div[2]/a/button")

        # Click the manage institution buttons
        btnCreateFac.click()

        # Get manage institution title
        createFacTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (createFacTitle.text == "Add new Faculty:")
    
    def test_create_new_faculty(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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

        # Open the create faculty page
        ff_browser.get(application + "/create_faculty")

        # Get faculty name input
        facName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Send value for new faculty
        facName.send_keys(newFacTest)

        # Get save faculty button
        btnSaveFac = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveFac.click()

        # Get title element
        titleSaved = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (titleSaved.text == "Manage Faculties:")

    def test_create_new_faculty_wrong_name(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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

        # Open the create faculty page
        ff_browser.get(application + "/create_faculty")

        # Get faculty name input
        facName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Send value for new faculty
        facName.send_keys(faculty_test)

        # Get save faculty button
        btnSaveFac = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveFac.click()

        # Get title element
        titleWrongName = ff_browser.find_element_by_xpath("/html/body/div[2]/p[1]")

        assert (titleWrongName.text == "Faculty already exists")

    def test_edit_faculty_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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
        ff_browser.get(application + "/manage_faculties")

        # Get selection of faculty box
        faculty = Select(ff_browser.find_element_by_name("faculty"))

        # Select the faculty for test
        faculty.select_by_visible_text(faculty_test)

        # Get edit faculty button
        btnEditFac = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/a/button")

        # Click the edit faculty buttons
        btnEditFac.click()

        # Get manage faculty title
        editFacTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (editFacTitle.text == "Edit Faculty:")
    
    def test_edit_faculty(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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

        # Open the edit faculty page
        ff_browser.get(application + "/edit_faculty/" + str(facID))

        # Get faculty name input
        facName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Clear facName before entering value
        facName.clear()

        # Send value for new faculy
        facName.send_keys(newFacTest)

        # Get save faculty button
        btnSaveFac = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveFac.click()

        # Get title element
        titleSaved = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (titleSaved.text == "Manage Faculties:")
    
    def test_edit_faculty_existing_name(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
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

        # Open the edit faculty page
        ff_browser.get(application + "/edit_faculty/" + str(facID))

        # Get faculty name input
        facName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")
        
        # Clear facName before entering value
        facName.clear()

        # Send value for new faculty
        facName.send_keys(faculty_test)

        # Get save faculty button
        btnSaveFac = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveFac.click()

        # Get title element
        titleWrongName = ff_browser.find_element_by_xpath("/html/body/div[2]/p[1]")

        assert (titleWrongName.text == "Faculty already exists")
    
    def test_not_admin_manage_faculty_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/manage_faculties")

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")

    def test_not_admin_create_faculty_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/create_faculty")

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")

    def test_not_admin_edit_faculty_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_fac):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/edit_faculty/" + str(facID))

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")