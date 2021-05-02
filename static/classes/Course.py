class Course():
    """
    Class for object of Course that constructed from course id and name
    """

    def __init__(self, id, name,lecturer = "",year = 1):
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