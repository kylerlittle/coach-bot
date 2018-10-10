import datetime
from workout import Workout
# from user import User

class Calendar:
	_events = []

	def __init__(self,user=None):
		# self._user = user
		pass
	def __str__(self):
		s = ""
		for i in self._events:
			s += str(i)
		return s
	# def getUser(self):
	# 	return self._user
	def addToCalendar(self, evnt):
		#if not isinstance(evnt, Event):
		if False:
			print ('Unexpected argument type\n\tExpected type: Event | Got Type: ' + str(type(evnt))) 
		else:
			inserted = False
			for i in range(0,len(self._events)-1):
				if (((evnt._start-datetime.datetime.now()).days
							 > (self._events[i]._startDateTime-datetime.datetime.now()).days)
					and ((evnt._startDateTime-datetime.datetime.now()).days
							 > (self._events[i+2]._startDateTime-datetime.datetime.now()).days)):
					self._events.insert(i+1,evnt)
					inserted = True
					break
			if not inserted:
				self._events.append(evnt)
	def showWorkouts(self):
		for i in self._events:
			if (isinstance(i, Workout)):
				print(i)
	def showWorkoutsDay(self,day):
		for i in events:
			if (isinstance(i, Workout) and (i._startDateTime == day)):
				print(i)
	def showEventsDay(self,day):
		for i in events:
			if i._startDateTime == day:
				print(i)
	def findEvent(self,iden):
		for i in events:
			if i._id == iden:
				return i
		return 0
	def export(self):
		xmlstr = "<calendar id={i}>\n".format(self._calendarId)
		xmlstr += "\t<events>\n"
		for event in self._events:
			xmlstr += "\t\t<event id={0}>\n".format(event.getId())
			xmlstr += "\t\t\t<description>{0}</description>\n".format(event.getDescription())	
			xmlstr += "\t\t\t<location>{0}<\location>\n".format(event.getLocation())
			xmlstr += "\t\t\t<start>{0}<\start>\n".format(event.getStartDate())
			xmlstr += "\t\t\t<end>{0}<\end>\n".format(event.getEndDate())
			xmlstr += "\t\t<\event>\n"
		xmlstr += "\t<\events>"
		xmlstr += "<\calendar>"
		return xmlstr	



















