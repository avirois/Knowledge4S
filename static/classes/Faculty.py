class Faculty():
    """
    Class for object of Faculy that constructed from faculty id and name
    """

    def __init__(self, id, name):
        """Ctor function for object of faculty"""
        self.id = id
        self.name = name

    def getID(self):
        """The function retruns id of faculty"""
        return (self.id)

    def getName(self):
        """The function retruns name of faculty"""
        return (self.name)

    def setName(self, name):
        """The function sets new name for faculty"""
        self.name = name

    def validateFaculty(self):
        """ The function validates the faculty name """
        return (self.getName() != "")