from event import Event
from feedback import FeedBack
from user import User
import datetime 

class Workout(Event):

    def __init__(self):
        self._feedback = FeedBack()
        self._calories = 0
        self.tags = [""]
        Event.__init__(self)

    def Workout(self, id = 0, calendarId = 0, 
    description = "", location = "", startDateTime = datetime.datetime(), 
    endDateTime = datetime.datetime(), user = User(), feedback = "", calories = 0, tags = [""]):
        self._feedback = feedback
        self._calories = calories
        self.tags = tags
        Event.Event(id, calendarId, description, location, startDateTime, endDateTime, user)

    def setFeedBack(self, feedBack):
        self._feedback(feedBack)

    def __str__(self):
        #fill this in 
        return (str("TODO"))    