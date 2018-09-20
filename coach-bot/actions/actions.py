"""
If not all details are provided to perform the action,
ASSUME REASONABLE DEFAULTS. We will generally confirm
with the user before doing something.
"""


# Generic Action class
class Action:
    def __init__(self):
        self.details = {}

    # Function members
    
    # Execute the action here
    # (): void
    def execute(self):
        print("yay execution")
        
# Action subclasses here...
class HelpAction(Action):
    def execute(self):
        print("HELP ME")

class ScheduleWorkoutAction(Action):
    def execute(self):
        print("Scheduling workout")

class DisplayCalendarScheduleAction(Action):
    def execute(self):
        print("Displaying calendar")

class DisplayWorkoutStatsAction(Action):
    def execute(self):
        print("Displaying workout stats")

class DisplayWorkoutScheduleAction(Action):
    def execute(self):
        print("Displaying workout schedule")

class SetFeedbackAction(Action):
    def execute(self):
        print("Setting feedback")

class SetCaloriesAction(Action):
    def execute(self):
        print("Setting calories")