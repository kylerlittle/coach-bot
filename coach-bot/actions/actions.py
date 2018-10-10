"""
:notes
> If not all details are provided to perform the action,
  assume reasonable default. We will generally confirm
  with the user before doing something.
> This is a big TODO.
> This needs a lot of work. We don't even account for which user is which, and we
  completely neglect the details that the user gives us (stored in self.details).
"""
from event_calendar import Calendar
from event import Event
from feedback import FeedBack

# Abstract Base Action Class
class Action:
    def __init__(self, _details={}):
        self.details = _details
        self.current_calories = 0
        self.current_stats = 25
        self.calendar = Calendar()
        self.fb = FeedBack()

    def execute(self):
        raise NotImplementedError('Action is an abstract base class; execute() is purely virtual.')
        
# Action subclasses here...
class HelpAction(Action):
    def execute(self):
        print("1. Enter a verb.")
        print("   - Plan")
        print("   - Schedule")
        print("   - Enter")
        print("   - Display")
        print("2. Enter a noun.")
        print("   - most recent workout")
        print("   - workout schedule")
        print("   - feedback")
        print("   - workout stats")
        print("3. Optionally specify a time.")
        print("   - on Tuesday")
        print("   - for tomorrow")
        print("   - at 5PM tomorrow")
        print("e.g. Display my most recent workout")

class ScheduleWorkoutAction(Action):
    def execute(self):
        # Create event
        e = Event()
        desc = input("Enter the description of the work out: ")
        loc = input("Enter the location: ")
        e.updateDescription(desc)
        e.updateLocation(loc)

        # Add to calendar
        self.calendar.addToCalendar(e)
        
class DisplayCalendarAction(Action):
    def execute(self):
        print("Your Calendar:")
        print(self.calendar)

class DisplayWorkoutStatsAction(Action): 
    def execute(self):
        print(self.current_stats)

class DisplayWorkoutScheduleAction(Action):
    def execute(self):
        print(self.details)
        self.calendar.showWorkouts()

class SetFeedbackAction(Action):
    def execute(self):
        r = input("How would you rate this:")
        self.fb.setRating(r)
        c = input("Give us a comment:")
        self.fb.setComment(c)

class SetCaloriesAction(Action):
    def execute(self):
        print(self.details)
        self.calories = input("Setting the calorie intake:")