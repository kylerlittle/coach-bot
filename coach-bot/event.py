import datetime
from user import User

class Event:
    def __init__(self):
        self._id = -1
        self._calendarId = -1
        self._description = ""
        self._location = ""
        self._startDateTime = datetime.datetime.now()
        self._endDateTime = datetime.datetime.now() + datetime.timedelta(minutes=60)
        self._user = User()
    
    def Event(self, id = 0, calendarId = 0, 
    description = "", location = "", startDateTime = datetime.datetime.now(), 
    endDateTime = datetime.datetime.now(), user = User()):
        self._id = id
        self._calendarId = calendarId
        self._description = description
        self._location = location
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime
        self._user = user

    #update setters
    def updateStartTime(self, newDateTime):
        self._startDateTime = newDateTime
    
    def updateEndTime(self, newDateTime):
        self._endDateTime = newDateTime

    def updateDescription(self, newDescription):
        self._description = newDescription

    def updateLocation(self, newLocation):
        self._location = newLocation

    #overwrite str
    def __str__(self):
        return str(
            ("----------\nid: {0}\ncalendarId: {1}\ndescription: {2}",
            self._id, self._calendarId, self._description)+
            ("\nstart time: {0}\nend time: {1}\nuser: {2}\n----------",
            self._startDateTime, self._endDateTime, self._user)
        )
    
    def getCalendarId(self):
        return self._calendarId
    
    def getId(self):
        return self._id
    
    def getDescription(self):
        return self._description
    
    def getLocation(self):
        return self._location
    
    def getStartDate(self):
        return self._startDateTime
    
    def getEndDate(self):
        return self._endDateTime


