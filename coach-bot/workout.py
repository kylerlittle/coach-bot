from event import Event
from feedback import FeedBack
import datetime 

class Workout(Event):

    def __init__(self, id = 0, calendarId = 0, 
    description = "", location = "", startDateTime = datetime.datetime.now(), 
    endDateTime = datetime.datetime.now(), userId = -1, feedback = "", calories = 0, tags = [""]):
        self._feedback = FeedBack()
        self._calories = 0
        self._tags = [""]
        Event.__init__(self)

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

    def export(self):
		xmlstr += "\t\t<Workout id={0}>\n".format(self.id)
			xmlstr += "\t\t\t<Feedback>{0}<\Feedback>\n".format(self._feedback)	
			xmlstr += "\t\t\t<Calories>{0}<\Calories>\n".format(self._calories)
			xmlstr += "\t\t\t<Tags>{0}<\Tags>\n".format(self._tags)
		    xmlstr += "<\Workout>"
    

    
        