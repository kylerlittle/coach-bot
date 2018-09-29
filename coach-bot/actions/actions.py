"""
:notes
> If not all details are provided to perform the action,
  assume reasonable default. We will generally confirm
  with the user before doing something.
> This is a big TODO.
"""
import sys
import calendar from CalendarClass
sys.path.append(/Users/shusantabhattarai/coach-bot/coach-bot/CalendarClass.py)
from CalendarClass import Calendar
# Generic Action class
 
class Action:
    def __init__(self, _details={}):
        self.current_calories = 0
        self.current_stats = 25
        self.calendar = Calendar()


    # Function members
    
    # Execute the action here
    # (): void
    def execute(self):
        print("yay execution")
        
# Action subclasses here...
class HelpAction(Action):
    def execute(self):
        print( "Set your calorie intake and chose a workout!")

class ScheduleWorkoutAction(Action): ''' need help from chris '''
    def execute(self):
        print(self.details)
        
class DisplayCalendarAction(Action):
    def execute(self):
        print(self.details)
        print("Displaying calendar")

class DisplayWorkoutStatsAction(Action): 
    def execute(self):
        print(self.current_stats)

class DisplayWorkoutScheduleAction(Action):
    def execute(self):
        print(self.details)
        self.calendar.showWorkouts()

class SetFeedbackAction(Action):
    def execute(self):
        print(self.details)
        print("Setting feedback") 

class SetCaloriesAction(Action):
    def execute(self):
        print(self.details)
        self.calories = input("Setting the calorie intake:")