import spacy
import parsedatetime
from datetime import datetime
import pytz
from pytz import timezone
from actions.actions import *

"""
:notes
> Always try to use lemma_ when possible versus the raw str text, since
  lemma_ returns the base form of the token, with no inflectional suffixes
  and all lowercase.
> Use the developer-defined thesaurus to help understand what the user
  is trying to do.
"""

MODEL_DIR = './coach-bot/nlp/model'  # this is the relative path from the project's root dir
DEFAULT_TIMEZONE = "US/Pacific"  # we could leverage a third-party library to localize this, but this is fine for now
cal = parsedatetime.Calendar()  # declare main object of parsedatetime module

"""
Define any synonyms for words user might use here.
"""
thesaurus = {
    "schedule_verb": ["schedule", "plan", "request"],
    "display": ["display", "show", "see"],
    "enter": ["enter", "set"],
    "workout": ["workout", "exercise"],
    "schedule_noun": ["schedule", "calendar"],
    "statistics": ["statistics", "stats", "statistic", "stat"],
    "feedback": ["feedback", "response"],
    "calories": ["calories", "calorie"],
    "help": ["help", "assist"]
}

class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class NaturalLanguageProcessor:
    @staticmethod
    def process_input(input_str):
        """Process user's input by returning an Action.

        :params
        input_str -- raw input text from user
        """
        tokenized = NaturalLanguageProcessor.return_tokenized([input_str])
        action, err = NaturalLanguageProcessor.tokens_to_action(tokenized)
        if action is None:
            raise InputError(input_str, err)
        return action

    @staticmethod
    def return_tokenized(text):
        """Tokenize the user's input text based on nlp model we trained.

        :params
        text -- raw input text from user
        """
        nlp = spacy.load(MODEL_DIR)
        docs = nlp.pipe(text)
        for doc in docs:
            if doc is not None:
                return [t for t in doc if t.dep_ != '-']

    @staticmethod
    def get_time_toks(tok_list):
        """Filter token list to only tokens with TIME label.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        """
        return list(filter(lambda t: t.dep_ == 'TIME', tok_list))

    @staticmethod
    def get_time_str(time_tok_list):
        """Join time tokens into a string, so datetimeparse can process it.

        :params
        time_tok_list -- list of spaCy Tokens with TIME label
        """
        return " ".join([t.text for t in time_tok_list])

    @staticmethod
    def get_datetime_from_str(time_str):
        """Return datetime object from natural language time string using datetimeparse module.

        :params
        time_str -- a datetime-like string in natural language (e.g. 'tomorrow at 5PM')
        """
        datetime_obj, _ = cal.parseDT(datetimeString=time_str, tzinfo=timezone(DEFAULT_TIMEZONE))
        return datetime_obj

    @staticmethod
    def get_datetime_from_tok_list(tok_list):
        """Return datetime object directly from the token list.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        """
        return NaturalLanguageProcessor.get_datetime_from_str(
            NaturalLanguageProcessor.get_time_str(
                NaturalLanguageProcessor.get_time_toks(tok_list)
            )
        )

    @staticmethod
    def get_root_action(tok_list):
        """Return the root action from the token list.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        """
        try:
            return tok_list[[t.dep_ for t in tok_list].index('ROOT')].lemma_
        except ValueError:
            return ""

    @staticmethod
    def get_action_receiver(tok_list):
        """Return the action receiver from the token list.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        """
        try:
            return tok_list[[t.dep_ for t in tok_list].index('WHAT')].lemma_
        except ValueError:
            return ""

    @staticmethod
    def get_action_receiver_attrs(tok_list, action_receiver):
        """Return the action receiver attributes from token list.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        action_receiver -- lemma_ of token from token list with dep_ == 'WHAT'
        """
        return [t.lemma_ for t in tok_list if t.dep_ == "ATTRIBUTE" and t.head.lemma_ == action_receiver]

    @staticmethod
    def initially_process_toks(tok_list):
        """Return root action, action receiver, the action receiver's attributes, and
        a datetime object from the token list.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        """
        root_action = NaturalLanguageProcessor.get_root_action(tok_list)
        action_receiver = NaturalLanguageProcessor.get_action_receiver(tok_list)
        action_receiver_attrs = NaturalLanguageProcessor.get_action_receiver_attrs(tok_list, action_receiver)
        datetime_obj = NaturalLanguageProcessor.get_datetime_from_tok_list(tok_list)
        return root_action, action_receiver, action_receiver_attrs, datetime_obj
    
    @staticmethod
    def tokens_to_action(tok_list):
        """Return an (Action, Error Message) tuple based on token list.

        :params
        tok_list -- list of spaCy Tokens as determined by the nlp model where we trained intent
        """
        action = None
        err = ""
        try:
            root_action, action_receiver, action_receiver_attrs, datetime_obj = NaturalLanguageProcessor.initially_process_toks(tok_list)
            if (root_action in thesaurus["schedule_verb"]):  # user wants to schedule something
                action = ScheduleWorkoutAction({"tags": action_receiver_attrs, "time": datetime_obj})
            elif (root_action in thesaurus["display"]):  # user wants to display something
                if action_receiver in thesaurus["schedule_noun"]:  # user wants to display schedule
                    # If action_receiver_attrs contains a synonym for "workout", display workout schedule
                    for attr in action_receiver_attrs:
                        if attr in thesaurus["workout"]:
                            action = DisplayWorkoutScheduleAction({"time": datetime_obj})
                            break
                    else:  # Otherwise, display normal calendar by default.
                        action = DisplayCalendarAction({"time": datetime_obj})
                elif action_receiver in thesaurus["statistics"]:  # user wants to display statistics (assume workout stats!)
                    action = DisplayWorkoutStatsAction({"time": datetime_obj})
                else:  # Unsure what the user wants to display
                    err = "Unsure how to display {what}".format(what=action_receiver)
            elif (root_action in thesaurus["enter"]):  # user wants to enter something
                if action_receiver in thesaurus["feedback"]:  # user wants to enter feedback
                    action = SetFeedbackAction({"time": datetime_obj})
                elif action_receiver in thesaurus["calories"]:  # user wants to enter calories
                    action = SetCaloriesAction({"time": datetime_obj})
                else:  # Unsure what the user wants to enter
                    err = "Unsure how to enter {what} into the system".format(what=action_receiver)
            elif (root_action in thesaurus["help"]):  # user wants help
                action = HelpAction()
            else:  # otherwise, we're not sure what the user wants.
                err = "Unsure how to handle action: {action}".format(action=root_action)
        except Exception as excp:
            err = "Error during processing of input.\nFrom interpreter: {err_msg}".format(err_msg=excp)
        return action, err
