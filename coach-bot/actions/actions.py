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
import datetime
from event_calendar import Calendar
from workout import Workout
from event import Event
from feedback import FeedBack
from rating import Rating

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

# TODO: Need a method to figure out what workout obj user wants
#       from calendar
# Classes: DisplayWorkoutStatsAction
#          SetFeedBackAction
#          SetCaloriesAction
# All it does now is return the first workout obj in the list.

# TODO: Need an edit workout function for Calendar class
#       Not sure if the current implementation actually
#       changes the workout object reference from the calendar or not

# Abstract Base Action Class
class Action:
    def __init__(self, _details={}):
        self.details = _details
        self.current_calories = 0
        self.current_stats = 25
        self.calendar = Calendar()
        self.fb = FeedBack()

    def getDetails(self):
        return self.details

    def setDetails(self, _details):
        self.details = _details

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

        # Create workout event
        e = Workout()
        loc = input("Enter the location: ")
        calo = input("Enter calories to be burned: ")
        if "tags" in self.details:
            e.setTags(self.details["tags"])
            for tag in self.details["tags"]:
                e.updateDescription(self.details["tags"])
        if "time" in self.details:
            e.updateStartTime(self.details["time"])
        e.updateLocation(loc)
        e.setCalories(calo)

        # User verification
        #print(e) # Cannot print out Workout
        resume = input("Is this what you wanted to add? (y/n): ")
        while resume != 'y':
            print("Start time")
            print("End time")
            print("Description")
            print("Location")
            print("Calories")
            e_change = input("What would you like to change?: ")
            newData = input("Set it here: ")

            # Is there an easier way to process user input?
            if e_change == "Start time":
               datetime_obj, _ = cal.parseDT(datetimeString=newData, tzinfo=timezone(DEFAULT_TIMEZONE))
               e.updateStartTime(datetime_obj) 

            elif e_change == "End time":
               datetime_obj, _ = cal.parseDT(datetimeString=newData, tzinfo=timezone(DEFAULT_TIMEZONE))
               e.updateEndTime(datetime_obj)

            elif e_change == "Description":
               e.updateDescription(newData)

            elif e_change == "Location":
                e.updateLocation(newData)

            elif e_change == "Calories":
                e.setCalories(newData)

            else:
                print("Invalid request to change.")

            #print(e)
            resume = input("Retry change? (y/n): ")

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
        # Get workout instance
        if "time" in self.details:
           ws = self.calendar.getWorkout(self.details["time"])
           if ws is None:
               print("No such workout exists.")
           else:
               w = ws[0] # Get first workout instance
               # Get duration of workout
               diff = w.getEndDate() - w.getStartDate()
               dur = divmod(diff.days * 86400 + diff.seconds, 60)
               print("Duration: {%M:%S}".format(dur))

               print("Calories: " + w.getCalories())
               print("Tags: ")
               for tag in self.details["tags"]:
                   print(tag + "/")
        else:
            print("Unsure what workout is specified.")

# Display workout events on calendar
# If a time is given, show events only at that time
class DisplayWorkoutScheduleAction(Action):
    def execute(self):
        if "time" in self.details:
            self.calendar.showWorkoutsDay(self.details["time"])
        else:
            self.calendar.showWorkouts()

# Set feeback of the workout event
class SetFeedbackAction(Action):
    def execute(self):

        # Get workout event
        if "time" in self.details:
            ws = self.calendar.getWorkout(self.details["time"])
            if ws is None:
                print("No such workout exists")
            else:
                w = ws[0] # Get first workout instance
                # Create new feedback
                f = FeedBack()
                r = input("How would you rate this workout out of 5: ")
                f.setRating(r)
                c = input("Give us a comment: ")
                f.setComment(c)

                # Edit workout event feedback
                w.setFeedBack(f)
        else:
            print("Unsure what workout is specified.")

# Set calories of the workout event 
class SetCaloriesAction(Action):
    def execute(self):
        
        # Get workout event
        if "time" in self.details:
            ws = self.calendar.getWorkout(self.details["time"])
            if ws is None:
                print("No such workout exists")
            else:
                w = ws[0] # Get first workout
                c = input("Setting the calorie intake: ")
                w.setCalories(c)
        else:
            print("Unsure what workout is specified.")
