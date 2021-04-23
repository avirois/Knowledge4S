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
email = "aaa@aaa.com"

@pytest.fixture
def db_prepare_manage_users():
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
        con.execute(sqtInsertUser, (username_test, "test1", "test1", encryptPassword(password_test), instID, facID, 2, email))
    
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

    # Commit the changes in users table
    con.commit()

    # CLose connection to DB
    con.close()

class TestIntegrationManageUsers:
    
    def test_manage_users_page(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_users):
        
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

        # Get manage users button
        btnManageUsers = ff_browser.find_element_by_name("usersManage")

        # Click the manage users button
        btnManageUsers.click()

        # Get manage institution title
        manageUsersTitle = ff_browser.find_element_by_name("titleManageUsers")

        assert (manageUsersTitle.text == "Manage Users:")

    def test_ban_user(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_users):
        
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

        # Open the manage users page
        ff_browser.get(application + "/manage_users")

        # Get ban test user button
        btnBanTestUser = ff_browser.find_element_by_id(username_test + "_banBtn")

        # Click the manage users button
        btnBanTestUser.click()

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

        # Get the banned message element
        bannedMsg = ff_browser.find_element_by_xpath("/html/body/div[2]/b")
        
        assert bannedMsg.text == ("Your user is banned!")

    def test_unban_user(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_users):
        
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

        # Open the manage users page
        ff_browser.get(application + "/manage_users")

        # Get ban test user button
        btnBanTestUser = ff_browser.find_element_by_id(username_test + "_banBtn")

        # Click the ban user button
        btnBanTestUser.click()

        # Get unban test user button
        btnUnbanTestUser = ff_browser.find_element_by_id(username_test + "_unbanBtn")

        # Click the unban user button
        btnUnbanTestUser.click()

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

        # Get the welocme message element
        welcomeMsg = ff_browser.find_element_by_name("welcome_message")
        
        assert welcomeMsg.text == ("Welcome " + username_test + "!")

    def test_add_admin(self, application: str, ff_browser: webdriver.Firefox, db_prepare_manage_users):
        
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

        # Open the manage users page
        ff_browser.get(application + "/manage_users")

        # Get revoke admin test user button
        btnRevokeAdmin = ff_browser.find_element_by_id(username_test + "_revokeBtn")

        # Click the revoke admin
        btnRevokeAdmin.click()

        # Get grant admin test user button
        btnGrantAdmin = ff_browser.find_element_by_id(username_test + "_grantBtn")

        # Click the grant admin
        btnGrantAdmin.click()

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

        # Get control panel button
        controlPanelBtn = ff_browser.find_element_by_name("control_panel_link")
        
        assert controlPanelBtn.text == ("Control Panel")
