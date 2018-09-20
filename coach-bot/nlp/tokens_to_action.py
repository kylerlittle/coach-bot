import spacy
import parsedatetime
from datetime import datetime
import pytz
from pytz import timezone

MODEL_DIR = './model'
DEFAULT_TIMEZONE = "US/Pacific"

cal = parsedatetime.Calendar()

# Could probably just use functions in this file, but might be a good opportunity to use an anti-pattern!

def return_tokenized(text):
    nlp = spacy.load(MODEL_DIR)
    docs = nlp.pipe(text)
    for doc in docs:
        if doc is not None:
            return [t for t in doc if t.dep_ != '-']
        #return [(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != '-']

def get_time_toks(tok_list):
    return list(filter(lambda t: t.dep_ == 'TIME', tok_list))

def get_time_str(time_tok_list):
    return " ".join([t.text for t in time_tok_list])

def get_datetime_from_str(time_str):
    datetime_obj, _ = cal.parseDT(datetimeString=time_str, tzinfo=timezone(DEFAULT_TIMEZONE))
    return datetime_obj

# Testing stuff...
test_text = ["Schedule me a leg workout for 5PM tomorrow"]
test1_toks = return_tokenized(test_text)
print(test1_toks)
print(get_time_toks(test1_toks))
time_str = get_time_str(get_time_toks(test1_toks))
print(time_str)
datetime_obj = get_datetime_from_str(time_str)
print(datetime_obj)

