class Institution():
    """
    Class for object of institution that constructed from institution id and name
    """

    def __init__(self, id, name):
        """Ctor function for object of institution"""
        self.id = id
        self.name = name

    def getID(self):
        """The function retruns id of institution"""
        return (self.id)

    def getName(self):
        """The function retruns name of institution"""
        return (self.name)

    def setName(self, name):
        """The function sets new name for institution"""
        self.name = name

    def validateInstitution(self):
        """ The function validates the institution name """
        return (self.getName() != "")