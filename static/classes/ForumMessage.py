class ForumMessage():
    """
    Class for object of Forum Message that constructed from ID, CourseID, Date, UserName, Message, PreMessage
    """

    def __init__(self, ID, CourseID, Date, UserName, Message, PreMessage='-1', SubMessages=[]):
        """Ctor function for object of Forum Message"""
        self.ID = ID
        self.CourseID = CourseID
        self.Date = Date
        self.UserName = UserName
        self.Message = Message
        self.PreMessage = PreMessage
        self.SubMessages = SubMessages
    
    def getID(self):
        """The function retruns id of forum message"""
        return self.ID
    
    def getCourseID(self):
        """The function retruns course id of forum message"""
        return self.CourseID
    
    def getDate(self):
        """The function retruns date of forum message"""
        return self.Date
    
    def getUserName(self):
        """The function retruns username of forum message"""
        return self.UserName

    def getMessage(self):
        """The function retruns message of forum message"""
        return self.Message
    
    def getPreMessage(self):
        """The function retruns id of previouse message of forum message"""
        return self.PreMessage
    
    def getSubMessages(self):
        """The function retruns list of sub messages of forum message"""
        return self.SubMessages

    def setID(self, ID):
        """The function sets new id for forum message"""
        self.ID = ID
    
    def setCourseID(self, CourseID):
        """The function sets new course id for forum message"""
        self.CourseID = CourseID
    
    def setDate(self, Date):
        """The function sets new date for forum message"""
        self.Date = Date

    def setUserName(self, UserName):
        """The function sets new username for forum message"""
        self.UserName = UserName
    
    def setMessage(self, Message):
        """The function sets new message for forum message"""
        self.Message = Message

    def setPreMessage(self, PreMessage):
        """The function sets new previous message id for forum message"""
        self.PreMessage = PreMessage
    
    def setSubMessages(self, SubMessages):
        """The function sets list of sub messages for forum message"""
        self.SubMessages = SubMessages

    def validateMessage(self):
        return (self.getMessage() != "")

    def checkPreviousMessageExists(self):
        return (self.getPreMessage() != '-1')

    def checkSubMessagesExists(self):
        return (len(self.getSubMessages()) != 0)
    