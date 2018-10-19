# from event_calendar import Calendar
class User():

    def __init__(self):
        self.email = ""
        self.firstName = ""
        self.lastName = ""
        self.userId = ""
        # self.calendar = None

    def User(self, email="", firstName="", lastName="", userId=""):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.userId = userId

    def getFullName(self):
        fullName = self.firstName + " " + self.lastName
        return fullName

    def addCalendar(self):
        pass
        # self.calendar = Calendar()
    
    def getCalendar(self):
        pass
        # return self.calendar

    def getUserId(self):
        return self.userId
       
