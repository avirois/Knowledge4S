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
def db_prepare_manage_inst():
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

class TestManageInstitutions:
    def test_manage_institution_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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

        # Get manage institution button
        btnManageInst = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/a[1]/button")

        # Click the manage institution buttons
        btnManageInst.click()

        # Get manage institution title
        manageInstTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (manageInstTitle.text == "Manage Institutions:")
    
    def test_create_institution_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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
        ff_browser.get(application + "/manage_institutions")

        # Get manage institution button
        btnCreateInst = ff_browser.find_element_by_xpath("/html/body/div[2]/div[2]/a/button")

        # Click the manage institution buttons
        btnCreateInst.click()

        # Get manage institution title
        createInstTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (createInstTitle.text == "Add new institution:")
    
    def test_create_new_institution(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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

        # Open the create institution page
        ff_browser.get(application + "/create_institution")

        # Get institution name input
        instName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Send value for new institution
        instName.send_keys(newInstTest)

        # Get save institution button
        btnSaveInst = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveInst.click()

        # Get title element
        titleSaved = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (titleSaved.text == "Manage Institutions:")

    def test_create_new_institution_wrong_name(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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

        # Open the create institution page
        ff_browser.get(application + "/create_institution")

        # Get institution name input
        instName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Send value for new institution
        instName.send_keys(institution_test)

        # Get save institution button
        btnSaveInst = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveInst.click()

        # Get title element
        titleWrongName = ff_browser.find_element_by_xpath("/html/body/div[2]/p[1]")

        assert (titleWrongName.text == "Institution already exists")

    def test_edit_institution_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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
        ff_browser.get(application + "/manage_institutions")

        # Get selection of institution box
        institution = Select(ff_browser.find_element_by_name("institution"))

        # Select the institution for test
        institution.select_by_visible_text(institution_test)

        # Get manage institution button
        btnEditInst = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/a[1]/button")

        # Click the manage institution buttons
        btnEditInst.click()

        # Get manage institution title
        editInstTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (editInstTitle.text == "Edit institution:")

    def test_edit_institution(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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

        # Open the create institution page
        ff_browser.get(application + "/edit_institution/" + str(instID))

        # Get institution name input
        instName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Clear instName before entering value
        instName.clear()

        # Send value for new institution
        instName.send_keys(newInstTest)

        # Get save institution button
        btnSaveInst = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveInst.click()

        # Get title element
        titleSaved = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (titleSaved.text == "Manage Institutions:")

    def test_edit_institution_existing_name(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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

        # Open the create institution page
        ff_browser.get(application + "/edit_institution/" + str(instID))

        # Get institution name input
        instName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")
        
        # Clear instName before entering value
        instName.clear()

        # Send value for new institution
        instName.send_keys(institution_test)

        # Get save institution button
        btnSaveInst = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveInst.click()

        # Get title element
        titleWrongName = ff_browser.find_element_by_xpath("/html/body/div[2]/p[1]")

        assert (titleWrongName.text == "Institution already exists")

    def test_faculties_register_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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
        ff_browser.get(application + "/manage_institutions")

        # Get selection of institution box
        institution = Select(ff_browser.find_element_by_name("institution"))

        # Select the institution for test
        institution.select_by_visible_text(institution_test)

        # Get manage institution button
        btnFaculties = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/a[2]/button")

        # Click the manage institution buttons
        btnFaculties.click()

        # Get manage institution title
        registerFacultiesTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (registerFacultiesTitle.text == "Manage Faculties in Institutions:")

    def test_register_faculties_to_inst(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
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

        # Open the create institution page
        ff_browser.get(application + "/create_institution")

        # Get institution name input
        instName = ff_browser.find_element_by_xpath("/html/body/div[2]/form/p/input")

        # Send value for new institution
        instName.send_keys(newInstTest)

        # Get save institution button
        btnSaveInst = ff_browser.find_element_by_xpath("/html/body/div[2]/form/input")

        # Click on submit button
        btnSaveInst.click()

        # Get selection of institution box
        institution = Select(ff_browser.find_element_by_name("institution"))

        # Select the institution for test
        institution.select_by_visible_text(newInstTest)

        # Get manage institution button
        btnFaculties = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/a[2]/button")

        # Click the manage institution buttons
        btnFaculties.click()

        # Get faculty selection
        faculties = Select(ff_browser.find_element_by_name("faculty"))

        # Select faculty from list
        faculties.select_by_visible_text(faculty_test)

        # Save faculty button
        btnAddFac = ff_browser.find_element_by_xpath("/html/body/div[2]/div[1]/form/input")

        # Click on add button
        btnAddFac.click()

        # Get title after adding faculty to institution
        titleAddFac = ff_browser.find_element_by_xpath("/html/body/div[2]/p[1]")

        assert (titleAddFac.text == "Faculty registered!")

    def test_not_admin_manage_inst_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/manage_institutions")

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")

    def test_not_admin_create_inst_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/create_institution")

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")

    def test_not_admin_edit_inst_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/edit_institution/" + str(instID))

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")

    def test_not_admin_register_faculties_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_inst):
        # Run logout to clean session
        ff_browser.get(application + "/logout")
        
        # Open the control panel page
        ff_browser.get(application + "/register_faculty/" + str(instID))

        # Get manage institution title
        mainTitle = ff_browser.find_element_by_xpath("/html/body/div[2]/h1")

        assert (mainTitle.text == "Hello")