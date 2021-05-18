class File():
    """
    Class for object of file that constructed from FileID, UserName,
    FileName, Title, Description, DateUpload, DateModified, InstituteID, FacultyID, 
    CourseID, Approved, Type.
    """

    def __init__(self, FileID, UserName = "", FileName = "", Title = "",
                Description = "", DateUpload = "", DateModified ="",
                InstituteID = "", FacultyID = "", CourseID = "",
                Approved = False, Type = ""):
        """Ctor function for object of file"""
        self.FileID = FileID
        self.UserName = UserName
        self.FileName = FileName
        self.Title = Title
        self.Description = Description
        self.DateUpload = DateUpload
        self.DateModified = DateModified
        self.InstituteID = InstituteID
        self.FacultyID = FacultyID
        self.CourseID = CourseID
        self. Approved = Approved
        self.Type = Type

    def getFileID(self):
        return (self.FileID)

    def getUserName(self):
        return (self.UserName)

    def getFileName(self):
        return (self.FileName)

    def getTitle(self):
        return (self.Title)
    
    def getDescription(self):
        return (self.Description)
    
    def getDateUpload(self):
        return (self.DateUpload)

    def getDateModified(self):
        return (self.DateModified)
    
    def getInstituteID(self):
        return (self.InstituteID)

    def getFacultyID(self):
        return (self.FacultyID)
    
    def getCourseID(self):
        return (self.CourseID)

    def getApproved(self):
        return (self.Approved)
    
    def getType(self):
        return (self.Type)

    def setUserName(self, UserName):
        self.UserName = UserName

    def setFileName(self, FileName):
        self.FileName = FileName

    def setTitle(self, Title):
        self.Title = Title
    
    def setDescription(self, Description):
        self.Description = Description
    
    def setApproved(self, Approved):
        self.Approved = Approved
    
    def setType(self, Type):
        self.Type = Type

    def checkTitle(self):
        return (self.getTitle() != "")

    def checkDescription(self):
        return (self.getDescription() != "")