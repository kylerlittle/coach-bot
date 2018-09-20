"""
If not all details are provided to perform the action,
ASSUME REASONABLE DEFAULTS. We will generally confirm
with the user before doing something.
"""


# Generic Action class
class Action:
    def __init__(self, _details={}):
        self.details = _details

    # Function members
    
    # Execute the action here
    # (): void
    def execute(self):
        print("yay execution")
        
# Action subclasses here...
class HelpAction(Action):
    def execute(self):
        print(self.details)
        print("HELP ME")

class ScheduleWorkoutAction(Action):
    def execute(self):
        print(self.details)
        print("Scheduling workout")

class DisplayCalendarAction(Action):
    def execute(self):
        print(self.details)
        print("Displaying calendar")

class DisplayWorkoutStatsAction(Action):
    def execute(self):
        print(self.details)
        print("Displaying workout stats")

class DisplayWorkoutScheduleAction(Action):
    def execute(self):
        print(self.details)
        print("Displaying workout schedule")

class SetFeedbackAction(Action):
    def execute(self):
        print(self.details)
        print("Setting feedback")

class SetCaloriesAction(Action):
    def execute(self):
        print(self.details)
        print("Setting calories")