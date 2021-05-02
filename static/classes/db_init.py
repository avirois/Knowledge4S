import sqlite3,os,shutil
from User import encryptPassword

class DB_INIT:
    def __init__(self):
        self.db_name = 'database.db'
        self.user = "danny"
        self.pas = encryptPassword("!aA123123")
    def clean_DB(self):
        ''' remove all previous inserts from DB'''
        try:
            con = sqlite3.connect(self.db_name)
            con.execute("DELETE FROM Files")
            con.execute("DELETE FROM Courses")
            con.execute("DELETE FROM FacIn")
            con.execute("DELETE FROM Faculties")
            con.execute("DELETE FROM Institutions")
            con.execute("DELETE FROM Lecturers")
            con.execute("DELETE FROM Users")
            con.execute("DELETE FROM Comments")
            con.execute("DELETE FROM sqlite_sequence")
            con.commit()
            try:
                shutil.rmtree('storage/')
            except Exception as e:
                print(e)

            os.makedirs('storage')
        except Exception as e:
            print(e)
        finally:
            con.close()

    def add_DB(self):
        ''' add general data for testing '''
        try:
            con = sqlite3.connect(self.db_name)
            con.execute("INSERT into Institutions (InstitutionName) VALUES ('SCE')")
            con.execute("INSERT into Faculties (FacultyName) VALUES ('Software')")
            con.execute("INSERT into FacIn (InstitutionID,FacultyID) VALUES (1,1)")
            con.execute("INSERT into Lecturers (LecturerName,FacultyID,InstitutionID) VALUES ('BOB',1,1)")
            con.execute("INSERT into Courses (CourseName,LecturerID,Year) VALUES ('Databases',1,1)")
            con.execute("INSERT into Users (UserName,FirstName,LastName,Password,InstitutelID,FacultyID,StudyYear,Role) VALUES (?,'John','Doe',?,1,1,1,1)",(self.user,self.pas))
            con.commit()
        except Exception as e:
            print(e)
        finally:
            con.close()


db = DB_INIT()
# uncomment to reset db
db.clean_DB() 
# uncomment to insert default values into db
#db.add_DB()