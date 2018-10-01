import datetime
# from user import User
from datetime import timedelta

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
	def saveCalendar(self):
		#TODO: SAVE CALENDAR AS XML
		pass
	

