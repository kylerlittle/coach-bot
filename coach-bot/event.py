import datetime
import random

class Event:
    def __init__(self, id = -1, calendarId = 0, 
    description = "", location = "", startDateTime = datetime.datetime.now(), 
    endDateTime = datetime.datetime.now(), user = 0):
        #generate a random int
        if(id == -1):
            self._id = random.randint(0, 600)
        else:
             self._id = id
        self._calendarId = -1
        self._description = ""
        self._location = ""
        self._startDateTime = datetime.datetime.now()
        self._endDateTime = datetime.datetime.now() + datetime.timedelta(minutes=60)
        self._userId = -1
    

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
        return "----------\nid: {0}\ncalendarId: {1}\ndescription: {2}".format(
            self._id, self._calendarId, self._description) + \
                "\nstart time: {0}\nend time: {1}\nuser: {2}\n----------".format(
            self._startDateTime.date(), self._endDateTime.date(), self._userId)
    
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


