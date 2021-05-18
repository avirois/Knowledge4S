import sqlite3
from flask import current_app
from datetime import datetime
from static.classes.ForumMessage import ForumMessage

def parse_file_time(string):
    tmp = string.split(" ")
    date = tmp[0]
    time = tmp[1]
    date = date.split("-")
    time = time.split(":")
    return "{}/{}/{} - {}:{}".format(date[2],date[1],date[0],time[0],time[1])
class Course():
    """
    Class for object of Course that constructed from course id and name
    """

    def __init__(self, id, name="", lecturer = "",year = 1):
        """Ctor function for object of course"""
        self.id = id
        self.name = name
        self.lecturer = lecturer
        self.year = year

    def getID(self):
        """The function retruns id of course"""
        return (self.id)

    def getName(self):
        """The function retruns name of course"""
        return (self.name)

    def getLact(self):
        return self.lecturer

    def getYear(self):
        return self.year
    
    def setLact(self,lact):
        self.lecturer = lact
    
    def setYear(self,year):
        self.year = year

    def setName(self, name):
        """The function sets new name for course"""
        self.name = name

    def validateCourse(self):
        """ The function validates the course name """
        return ((self.getName() != "") and (self.getLact()!=""))

    def courseNameByID(self):
        """ The function gets the name of the course from the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryCourse = "SELECT CourseName FROM Courses WHERE CourseID = (?)"

        # Run the query to get institution data
        sqlRes = con.execute(sqlQuryCourse,(self.getID(),))

        # Fetch the result
        record = sqlRes.fetchone()

        # Check if course exists
        if (record != None):
            # Create course object for current selected courseID
            self.setName(record[0])

        # Close the connection to the database
        con.close()

        return (self.getName())

    def getSubMessagesOfMessage(self, messageID):
        """ The function gets the sub messages of a message in a course from the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryMessages = "SELECT UserName, Date, Message, ID FROM ForumMessages WHERE CourseID = (?) AND PreMessage = (?)"
        # get comments
        cur = con.execute(sqlQuryMessages, (self.getID(), messageID))

        # Initialize messages list
        messages = []

        # Run over the messages of the course and append them to list
        for row in cur:
            #tmp = (row[0], parse_file_time(row[1]), row[2], row[3])
            #messages.append(tmp)
            fMessage = ForumMessage(row[3], self.getID(), parse_file_time(row[1]), row[0], row[2], messageID)
            messages.append(fMessage)
        
        # Close the connection to the database
        con.close()

        return (messages)

    def getMessagesOfCourse(self):
        """ The function gets the messages of the course from the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryMessages = "SELECT UserName, Date, Message, ID FROM ForumMessages WHERE CourseID = (?) AND PreMessage ISNULL"
        # get comments
        cur = con.execute(sqlQuryMessages, (self.getID(),))

        # Initialize messages list
        messages = []

        # Run over the messages of the course and append them to list
        for row in cur:
            # Find sub messages
            subMessages = self.getSubMessagesOfMessage(row[3])

            #tmp = (row[0], parse_file_time(row[1]), row[2], row[3], subMessages)
            #messages.append(tmp)
            fMessage = ForumMessage(row[3], self.getID(), parse_file_time(row[1]), row[0], row[2], '-1', subMessages)
            messages.append(fMessage)
        
        # Close the connection to the database
        con.close()

        return (messages)
    
    def getSpecificMessageForum(self, messageID):
        """ The function gets a specific message of the course from the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryMessages = "SELECT UserName, Date, Message, ID, CourseID, PreMessage FROM ForumMessages WHERE ID = (?)"
        # get comments
        cur = con.execute(sqlQuryMessages, (messageID,))

        # Get the data from the result
        row = cur.fetchone()

        # Run over the messages of the course and append them to list
        if (row):
            #result = (row[0], parse_file_time(row[1]), row[2], row[3])
            result = ForumMessage(row[3], row[4], parse_file_time(row[1]), row[0], row[2], row[5])
        
        # Close the connection to the database
        con.close()

        return (result)

    def addMessageToCourse(self, message, user, preMessageID):
        """ The function gets message and adds it to the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Check if premessage exists
        if (preMessageID == "-1"):
            # Prepare the query
            sqlQuryNewMessage = "INSERT into ForumMessages (CourseID, Date, UserName, Message) VALUES (?,?,?,?)"

            # Execute the insert of message
            con.execute(sqlQuryNewMessage, (self.getID(), datetime.now(), user, message,))
        else:
            # Prepare the query if previous message exists
            sqlQuryNewMessage = "INSERT into ForumMessages (CourseID, Date, UserName, Message, PreMessage) VALUES (?,?,?,?,?)"

            # Execute the insert of message
            con.execute(sqlQuryNewMessage, (self.getID(), datetime.now(), user, message, preMessageID,))

        # commit the changes in the DB
        con.commit()
        
        # Close the connection to the database
        con.close()
    
    def deleteMessageForum(self, messageID):
        """ The function gets message ID and removes it to the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare query for sub messages delete
        sqlSubMessageDel = "DELETE FROM ForumMessages WHERE PreMessage = (?)"

        # Prepare the query
        sqlQuryDelMessage = "DELETE FROM ForumMessages WHERE ID = (?)"
        
        # Remove sub messages
        con.execute(sqlSubMessageDel, (messageID,))
        
        # Remove the message
        con.execute(sqlQuryDelMessage, (messageID,))

        # commit the changes in the DB
        con.commit()
        
        # Close the connection to the database
        con.close()
    
    def editMessageForum(self, messageID, newMessage):
        """ The function gets message ID and edit the message in the DB """
        # Connect to database and check if user exists
        con = sqlite3.connect(current_app.config['DB_NAME'])

        # Prepare the query
        sqlQuryDelMessage = "UPDATE ForumMessages SET Message = (?) WHERE ID = (?)"
        
        # set the edited message
        cur = con.execute(sqlQuryDelMessage, (newMessage, messageID,))

        # commit the changes in the DB
        con.commit()
        
        # Close the connection to the database
        con.close()