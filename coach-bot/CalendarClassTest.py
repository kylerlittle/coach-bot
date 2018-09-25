import datetime
from CalendarClass import *

class MockUser:
	def __init__(self,name):
		self._name = name
	def __str__(self):
		print(self._name)

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

class TestCalendar:
	def setup(self):
		self.user = None
		self.user = MockUser('TestUser') 
		self.cal = None
		self.cal = Calendar(self.user)

	def addToCalendarTest(self):
		self.setup()
		self.cal.addToCalendar(Workout('Legs',datetime.datetime(2018,11,9,0,0)))
		self.cal.addToCalendar(Workout('Arms',datetime.datetime(2018,9,19,0,0)))
		self.cal.addToCalendar(Workout('Chest',datetime.datetime(2018,10,10,0,0)))
		self.cal.addToCalendar(Workout('Tris',datetime.datetime.now()))
		for i in self.cal._events:
			print(str(i))	
		print('Expected results \"Tris,Arms,Chest,Legs\"') 
def main():
	tclass = TestCalendar()
	tclass.addToCalendarTest()

if __name__ == "__main__":
	main()	
