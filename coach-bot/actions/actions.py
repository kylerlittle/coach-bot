"""
:notes
> If not all details are provided to perform the action,
  assume reasonable default. We will generally confirm
  with the user before doing something.
> This is a big TODO.
> This needs a lot of work. We don't even account for which user is which, and we
  completely neglect the details that the user gives us (stored in self.details).
"""
from pytz import timezone
import parsedatetime
from event_calendar import Calendar
from workout import Workout
from event import Event
from feedback import FeedBack

DEFAULT_TIMEZONE = "US/Pacific"
cal = parsedatetime.Calendar()
debug = True

class ActionManager:
    def __init__(self, user_id):
        self._user_id = user_id
        self.pipeline = []

    def enqueue(self, action):
        action.setCalendar(self._user_id)
        self.pipeline.append(action)
        self.__run_jobs__()

    def __run_jobs__(self):
        while self.pipeline:
            action = self.pipeline.pop(0)  # dequeue front
            action.execute()

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
    
    def setCalendar(self, user_id):
        # self.calendar = calendar that matches user_id
        if debug: print(user_id)
        
# Action subclasses here...
class HelpAction(Action):
    def execute(self):
        print("1. Enter a verb.")
        print("   - Plan")
        print("   - Schedule")
        print("   - Enter")
        print("   - Display")
        print("   - Set")
        print("2. Enter a noun.")
        print("   - most recent workout")
        print("   - workout schedule")
        print("   - feedback")
        print("   - workout stats")
        print("   - calories")
        print("3. Optionally specify a time.")
        print("   - on Tuesday")
        print("   - for tomorrow")
        print("   - at 5PM tomorrow")
        print("e.g. Display my most recent workout")

# Create a Workout event and add to Calendar
class ScheduleWorkoutAction(Action):
    def execute(self):
        # Create event
        e = Event() #Workout()
        loc = input("Enter the location: ")
        if "tags" in self.details:
            e.updateDescription(self.details["tags"])
        if "time" in self.details:
            e.updateStartTime(self.details["time"])
        e.updateLocation(loc)

        # User verification
        print(e) # Cannot print out Workout
        resume = input("Is this what you wanted to add? (y/n): ")
        while resume == 'n':
            print("Start time")
            print("End time")
            print("Description")
            print("Location")
            e_change = input("What would you like to change?: ")

            # Not sure how to update time using user input
            # I would like to use the function from tokens_to_action
            # get_datetime_from_str

            # I would like to naturally process
            # what they would like to change
            print(e)
            resume = input("Is this what you wanted to add (y/n): ")

        # Add to calendar
        self.calendar.addToCalendar(e)

# Display all events on calendar
# If a time is given, show events only at that time
class DisplayCalendarAction(Action):
    def execute(self):
        print("Your Calendar:")
        if "time" in self.details:
            self.calendar.showEventsDay(self.details["time"])
        else:
            print(self.calendar)

# Display workout stats
class DisplayWorkoutStatsAction(Action): 
    def execute(self):
        print(self.current_stats)

# Display workout events on calendar
# If a time is given, show events only at that time
class DisplayWorkoutScheduleAction(Action):
    def execute(self):
        if "time" in self.details:
            self.calendar.showWorkoutsDay(self.details["time"])
        else:
            self.calendar.showWorkouts()

# TODO: use Workout class?
class SetFeedbackAction(Action):
    def execute(self):
        r = input("How would you rate this:")
        self.fb.setRating(r)
        c = input("Give us a comment:")
        self.fb.setComment(c)

# TODO: change calories of user??
class SetCaloriesAction(Action):
    def execute(self):
        print(self.details)
        self.calories = input("Setting the calorie intake:")
