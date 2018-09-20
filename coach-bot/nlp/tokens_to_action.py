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















import spacy
import parsedatetime
from datetime import datetime
import pytz
from pytz import timezone
#from actions import Action

"""
Always try to use lemma_ when possible versus the raw str text, since
lemma_ returns the base form of the token, with no inflectional suffixes
and all lowercase.
"""

MODEL_DIR = './model'
DEFAULT_TIMEZONE = "US/Pacific"
cal = parsedatetime.Calendar()
thesaurus = {
    "schedule_verb": ["schedule", "plan", "request"],
    "display": ["display", "show", "see"],
    "enter": ["enter", "set"],
    "workout": ["workout", "exercise"],
    "schedule_noun": ["schedule", "calendar"],
    "statistics": ["statistics", "stats", "statistic", "stat"],
    "feedback": ["feedback", "response"],
    "calories": ["calories", "calorie"]
}

def return_tokenized(text):
    nlp = spacy.load(MODEL_DIR)
    docs = nlp.pipe(text)
    for doc in docs:
        if doc is not None:
            return [t for t in doc if t.dep_ != '-']

def get_time_toks(tok_list):
    return list(filter(lambda t: t.dep_ == 'TIME', tok_list))

def get_time_str(time_tok_list):
    return " ".join([t.text for t in time_tok_list])

def get_datetime_from_str(time_str):
    datetime_obj, _ = cal.parseDT(datetimeString=time_str, tzinfo=timezone(DEFAULT_TIMEZONE))
    return datetime_obj

def get_datetime_from_tok_list(tok_list):
    return get_datetime_from_str(get_time_str(get_time_toks(tok_list)))

def tokens_to_action(tok_list):
    try:
        # Process tokens.
        root_action = tok_list[[t.dep_ for t in tok_list].index('ROOT')].lemma_
        action_receiver = tok_list[[t.dep_ for t in tok_list].index('WHAT')].lemma_
        action_receiver_attrs = [t.lemma_ for t in tok_list if t.dep_ == "ATTRIBUTE" and t.head.lemma_ == action_receiver]
        datetime_obj = get_datetime_from_tok_list(tok_list)
    except ValueError:
        print("No root action in this sentence. Bot unsure what to do.")
        return
    
    if (root_action in thesaurus["schedule_verb"]):  # user wants to schedule something
        return ScheduleWorkoutAction({"tags": action_receiver_attrs, "time": datetime_obj})
    elif (root_action in thesaurus["display"]):  # user wants to display something
        if action_receiver in thesaurus["schedule_noun"]:
            # If attrs contain a synonym for "workout", display workout schedule
            for attr in action_receiver_attrs:
                if attr in thesaurus["workout"]:
                    action = DisplayWorkoutScheduleAction({"time": datetime_obj})
                    break
            else:  # Otherwise, display normal calendar by default.
                action = DisplayCalendarAction({"time": datetime_obj})
            return action
        elif action_receiver in thesaurus["statistics"]:
            return DisplayWorkoutStatsAction({"time": datetime_obj})
        else:
            print("Unsure how to display {what}".format(what=action_receiver))
    elif (root_action in thesaurus["enter"]):
        if action_receiver in thesaurus["feedback"]:
            # if user doesn't supply a time, that's fine. If they do, then we'll use it to determine what workout
            # to give feedback on.
            return SetFeedbackAction({"time": datetime_obj})
        elif action_receiver in thesaurus["calories"]:
            return SetCaloriesAction()
        else:
            print("Unsure how to enter {what} into the system".format(what=action_receiver))
    else:
        print("Unsure what to do.")

# BASIC TESTING
test_texts = ["Schedule me a leg workout for 5PM tomorrow",
    "Display my workout calendar",
    "Enter my calories for today",
    "Display my normal calendar",
    "Show my workout statistics from yesterday",
    "Set feedback for my workout earlier at 3PM"]

for test_text in test_texts:
    tokenized = return_tokenized([test_text])
    action = tokens_to_action(tokenized)
    if action is not None:
        print("**************\nBot Processing: {user_input}\n**************".format(user_input=test_text))
        print("Bot Executing\n**************")
        action.execute()
        print("\n\n")