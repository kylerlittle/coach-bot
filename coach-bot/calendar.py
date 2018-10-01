import datetime
from user import *
from datetime import timedelta

class Event:
	def __init__(self,name,start):
		self._name=name
		self._start=start
	def __str__(self):
		print('Event:' + self._name + '    ' + self._start)

class Workout(Event):
	def __init__(self,name,start):
		Event.__init__(self,name,start)
	def __str__(self):
		return ('Workout:' + self._name + '    ' + str(self._start))

class Calendar:
	_events = []

	def __init__(self,user=None):
		self._user = user
	def __str__(self):
		print(self._events)
	def getUser(self):
		return self._user
	def addToCalendar(self, evnt):
		#if not isinstance(evnt, Event):
		if False:
			print ('Unexpected argument type\n\tExpected type: Event | Got Type: ' + str(type(evnt))) 
		else:
			inserted = False
			for i in range(0,len(self._events)-1):
				if (((evnt._start-datetime.datetime.now()).days
							 > (self._events[i]._start-datetime.datetime.now()).days)
					and ((evnt._start-datetime.datetime.now()).days
							 > (self._events[i+2]._start-datetime.datetime.now()).days)):
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
		for i in self._events:
			if (isinstance(i, Workout) and (i._start == day)):
				print(i)
	def saveCalendar(self):
		#TODO: SAVE CALENDAR AS XML
		pass
	

