import pytest
from static.classes.ForumMessage import ForumMessage
from datetime import datetime

class TestForumMessages:
    def test_valid_forum_message(self):
        ID = 1
        CourseID = 1
        Date = datetime.now()
        UserName = "Aviel"
        Message = "Testing forum message"
        PreMessage = "-1"
        SubMessages = []
        
        # Create message
        fmessage = ForumMessage(ID, CourseID, Date, UserName, Message, PreMessage, SubMessages)

        assert (fmessage.validateMessage())
    
    def test_invalid_forum_message(self):
        ID = 1
        CourseID = 1
        Date = datetime.now()
        UserName = "Aviel"
        Message = ""
        PreMessage = "-1"
        SubMessages = []
        
        # Create message
        fmessage = ForumMessage(ID, CourseID, Date, UserName, Message, PreMessage, SubMessages)

        assert (not fmessage.validateMessage())

    def test_no_prev_message_forum_message(self):
        ID = 1
        CourseID = 1
        Date = datetime.now()
        UserName = "Aviel"
        Message = ""
        PreMessage = "-1"
        SubMessages = []
        
        # Create message
        fmessage = ForumMessage(ID, CourseID, Date, UserName, Message, PreMessage, SubMessages)

        assert ( not fmessage.checkPreviousMessageExists())

    def test_prev_message_forum_message(self):
        ID = 1
        CourseID = 1
        Date = datetime.now()
        UserName = "Aviel"
        Message = ""
        PreMessage = "1"
        SubMessages = []
        
        # Create message
        fmessage = ForumMessage(ID, CourseID, Date, UserName, Message, PreMessage, SubMessages)

        assert (fmessage.checkPreviousMessageExists())

    def test_no_sub_message_forum_message(self):
        ID = 1
        CourseID = 1
        Date = datetime.now()
        UserName = "Aviel"
        Message = ""
        PreMessage = "-1"
        SubMessages = []
        
        # Create message
        fmessage = ForumMessage(ID, CourseID, Date, UserName, Message, PreMessage, SubMessages)

        assert ( not fmessage.checkSubMessagesExists())

    def test_exist_sub_messages_forum_message(self):
        ID = 1
        CourseID = 1
        Date = datetime.now()
        UserName = "Aviel"
        Message = ""
        PreMessage = "1"
        SubMessages = [ForumMessage(ID,CourseID,Date,UserName, Message)]
        
        # Create message
        fmessage = ForumMessage(ID, CourseID, Date, UserName, Message, PreMessage, SubMessages)

        assert (fmessage.checkSubMessagesExists())
