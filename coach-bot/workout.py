from event import Event
from feedback import FeedBack
import datetime 

class Workout(Event):

    def __init__(self, id = 0, calendarId = 0, 
    description = "", location = "", startDateTime = datetime.datetime.now(), 
    endDateTime = datetime.datetime.now(), userId = -1, feedback = "", ):
        self._feedback = FeedBack()
        self._calories = 0
        self._tags = [""]
        Event.__init__(self)

    def Workout(self, calories = 0, tags = [""]):
        self._feedback = feedback
        self._calories = calories
        self._tags = tags
        Event.Event()

    def setFeedBack(self, feedBack):
        self._feedback(feedBack)

    def getFeedback(self):
        return self._feedback

    def setCalories(self, calories):
        self._calories = calories

    def getCalories(self):
        return self._calories

    def setTags(self, tags):
        self._tags = tags

    def getTags(self):
        return self._tags

    def __str__(self):
        return "----------\n feedback: {0}\n calories: {1}\n tags: {2}".format(self._feedback, self._calories, self._tags)
        