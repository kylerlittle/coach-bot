
class User():

    def __init__(self):
        self.email = ""
        self.firstName = ""
        self.lastName = ""
        self.calendar = None

    def User(self, email="", firstName="", lastName=""):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName

    def getFullName(self):
        fullName = self.firstName + " " + self.lastName
        return fullName

    ##def addCalendar():
        ## TO DO
    

    ##def getCalendar():
        ## TO DO
