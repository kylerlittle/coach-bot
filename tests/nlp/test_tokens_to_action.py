import unittest
from unittest.mock import MagicMock, Mock, patch, call
from datetime import datetime
from pytz import timezone
import importlib
nlp = importlib.import_module("nlp.tokens_to_action")
act = importlib.import_module("actions.actions")

class MockToken(object):
    """Mock spaCy's Token Class, at least in terms of how it's
    used in TokensToActionConverter class.
    """
    def __init__(self, text, dep, lemma, head=None):
        self._text = text
        self._dep = dep
        self._lemma = lemma
        self._head = None if head is None else MockToken(head.text, head.dep_, head.lemma_)
    
    @property
    def text(self):
        return self._text

    @property
    def dep_(self):
        return self._dep

    @property
    def lemma_(self):
        return self._lemma

    @property
    def head(self):
        return self if self._head is None else self._head

class TestTokensToAction(unittest.TestCase):
    def setUp(self):
        # Construct an instance of TokensToActionConverter
        self.ttac = nlp.TokensToActionConverter()
        # Make test token lists here.
        self.tl1 = []
        self.tl2 = [MockToken('5 PM', 'TIME', '5 PM'), MockToken('tomorrow', 'TIME', 'tomorrow')]          # TIME only
        self.tl3 = [MockToken('schedule', 'ROOT', 'schedule'), MockToken('workout', 'WHAT', 'workout')] # all not TIME
        self.tl4 = self.tl3 + self.tl2   # Mixture of TIME and not TIME
        self.tl5 = [MockToken('arms', 'ATTRIBUTE', 'arm', self.tl4[1]), MockToken('cardio', 'ATTRIBUTE', 'cardio', self.tl4[1])]
        self.tl6 = [MockToken(x.text, x.dep_, x.lemma_) for x in self.tl5]  # exclude HEAD
        self.tl7 = self.tl4 + self.tl5
        

    def test_process_input(self):
        """Test process_input, which can either raise an InputError or return an action
        """
        # Stub return values for tokens_to_action.
        self.ttac.tokens_to_action = Mock(side_effect=[(None, "anything"), ("whatever", "anything")])
        self.assertRaises(nlp.InputError, self.ttac.process_input, self.tl1)           # assert
        self.ttac.tokens_to_action.assert_called_with(self.tl1)                        # verify
        self.assertEqual(self.ttac.process_input(self.tl2), "whatever")     # assert whatever is returned is same as stub[0]
        self.ttac.tokens_to_action.assert_called_with(self.tl2)             # verify

    def test_get_time_toks(self):
        """Test filtering of token list to just TIME token list.
        """
        self.assertFalse(self.ttac.get_time_toks(self.tl1))     # an empty list's truth value is False
        self.assertEqual(self.tl2, self.ttac.get_time_toks(self.tl2))   # all TIME toks should be same
        self.assertFalse(self.ttac.get_time_toks(self.tl3))     # an empty list's truth value is False
        self.assertEqual(self.tl2, self.ttac.get_time_toks(self.tl4))   # garbage should be filtered back to original

    def test_get_time_str(self):
        """Test getting time string from token list of only TIME tokens
        """
        self.assertTrue(self.ttac.get_time_str(self.tl1) == "")         # empty string for empty list
        self.assertEqual(self.ttac.get_time_str(self.tl2), "5 PM tomorrow")  # normal value
    
    @patch('coach-bot.nlp.tokens_to_action.parsedatetime.Calendar.parseDT')
    def test_get_datetime_from_str(self, mocked_parseDT):
        """Test getting a datetime object from natural language string. Since we use an external
        dependency to do this, we can mock its behavior.
        """
        # Stub return value for external dependency cal.parseDT
        mocked_parseDT.return_value = (datetime(2018, 10, 5), None)
        self.assertEquals(self.ttac.get_datetime_from_str(""), datetime(2018, 10, 5))
        mocked_parseDT.assert_called_once_with(datetimeString="", tzinfo=timezone('US/Pacific'))
        mocked_parseDT.reset_mock()  # reset mock call counter
        self.assertEquals(self.ttac.get_datetime_from_str("5 PM tomorrow"), datetime(2018, 10, 5))
        mocked_parseDT.assert_called_once_with(datetimeString="5 PM tomorrow", tzinfo=timezone('US/Pacific'))

    def test_get_datetime_from_tok_list(self):
        """Test getting datetime object from token list. Only need one test value since this
        method is merely a combination of several methods, and we use mocking to stub their return values.
        """
        # Stub method calls
        self.ttac.get_time_toks = Mock(return_value=self.tl2)
        self.ttac.get_time_str = Mock(return_value="5 PM tomorrow")
        self.ttac.get_datetime_from_str = Mock(return_value=datetime(2018, 10, 5))
        self.assertEquals(self.ttac.get_datetime_from_tok_list(self.tl1), datetime(2018, 10, 5))   # test
        # Verify mocks were called.
        self.ttac.get_time_toks.assert_called_once_with(self.tl1)
        self.ttac.get_time_str.assert_called_once_with(self.tl2)
        self.ttac.get_datetime_from_str.assert_called_once_with("5 PM tomorrow")

    def test_get_what_from_tok_list(self):
        """Test getting the first instance of token.lemma_ that satisfies dep_ == what (2nd arg)
        """
        self.assertEqual(self.ttac.get_what_from_tok_list(self.tl1, "WHAT"), "")  # test with empty list
        self.assertEqual(self.ttac.get_what_from_tok_list(self.tl4, "NOT_FOUND"), "")  # test with non-empty list, but unfound
        self.assertEqual(self.ttac.get_what_from_tok_list(self.tl4, "ROOT"), "schedule")  # test found in first pos
        self.assertEqual(self.ttac.get_what_from_tok_list(self.tl4, "WHAT"), "workout")   # test found in middle pos
        self.assertNotEqual(self.ttac.get_what_from_tok_list(self.tl4, "TIME"), "tomorrow") # test not found in last pos

    def test_get_action_receiver_attrs(self):
        """ Test getting action receiver attributes from the token list.
        """
        # Empty list => []
        self.assertEqual(self.ttac.get_action_receiver_attrs(self.tl1, 'workout'), [])
        # List with no ATTRIBUTE dep's ==> []
        self.assertEqual(self.ttac.get_action_receiver_attrs(self.tl4, 'workout'), [])
        # List with some ATTRIBUTE dep's ==> ['attr1', 'attr2', ...]
        self.assertEqual(self.ttac.get_action_receiver_attrs(self.tl7, 'workout'), ['arm', 'cardio'])
        # List with all ATTRIBUTE dep's ==> [] since no action_receiver supplied
        self.assertEqual(self.ttac.get_action_receiver_attrs(self.tl6, 'workout'), [])

    def test_initially_process_toks(self):
        """Test getting main components for natural language processing. Only one test needed since
        method is merely a combination of several methods, and we use mocking to stub their return values.
        """
        # Mock external function call return values.
        self.ttac.get_what_from_tok_list = Mock(side_effect=['schedule', 'workout'])
        self.ttac.get_action_receiver_attrs = Mock(return_value=['leg', 'cardio'])
        self.ttac.get_datetime_from_tok_list = Mock(return_value=datetime(2018, 11, 9))
        # Actual test on function's return value
        self.assertTupleEqual(('schedule', 'workout', ['leg', 'cardio'], datetime(2018, 11, 9)),
            self.ttac.initially_process_toks(self.tl1))
        # Verify behavior.
        self.ttac.get_what_from_tok_list.assert_has_calls([call(self.tl1, 'ROOT'), call(self.tl1, 'WHAT')])
        self.ttac.get_action_receiver_attrs.assert_called_once_with(self.tl1, 'workout')
        self.ttac.get_datetime_from_tok_list.assert_called_once_with(self.tl1)

    def test_tokens_to_action(self):
        """Test the main tokens_to_action function. Given a token list, this function outputs the appropriate
        Action subclass and error message (if any). This function tests this method using whitebox techniques.
        The number of assertions and mocks in this function demonstrates that tokens_to_action should probably
        be refactored.
        """
        # Need several mocks for self.ttac.initially_process_toks
        self.ttac.initially_process_toks = Mock(side_effect=[
            ('request', 'exercise', ['leg'], datetime(2018, 10, 19)),
            ('see', 'calendar', ['workout', 'other'], datetime(2018, 10, 19)),
            ('see', 'calendar', ['not workout synonym'], datetime(2018, 10, 19)),
            ('show', 'stats', [], datetime(2018, 10, 20)),
            ('display', '', ['workout'], datetime(2018, 10, 20)),
            ('set', 'feedback', ['workout'], datetime(2018, 11, 20)),
            ('enter', 'calorie', ['workout'], datetime(2018, 11, 20)),
            ('enter', '', ['workout'], datetime(2018, 11, 20)),
            ('assist', 'me', ['please'], datetime(2018, 12, 20)),
            ('', '', [], datetime(2018, 11, 20)),
            ('fdjskfldsjfls', 'fdlsjfld', ['sdf', 'sdfds'], datetime(2018, 11, 20))
            ])
        # 1. ROOT schedule verb synonym => Schedule a workout, no error
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.ScheduleWorkoutAction)
        self.assertEqual(err, "")
        self.assertEqual(a.getDetails().get("time", None), datetime(2018, 10, 19))
        self.assertEqual(a.getDetails().get("tags", None), ['leg'])
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
        # 2. ROOT display verb synonym
            # 2a. WHAT schedule noun synonym
                # 2a i. ATTRIBUTE workout synonym => Display Workout Calendar, no error
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.DisplayWorkoutScheduleAction)
        self.assertEqual(err, "")
        self.assertEqual(a.getDetails().get("time", None), datetime(2018, 10, 19))
        self.assertIsNone(a.getDetails().get("tags", None))
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
                # 2a ii. ATTRIBUTE has no workout synonym => Display Normal Calendar, no error
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.DisplayCalendarAction)
        self.assertEqual(err, "")
        self.assertEqual(a.getDetails().get("time", None), datetime(2018, 10, 19))
        self.assertIsNone(a.getDetails().get("tags", None))
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
            # 2b. WHAT statistics synonym => Display workout stats, no error msg
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.DisplayWorkoutStatsAction)
        self.assertEqual(err, "")
        self.assertEqual(a.getDetails().get("time", None), datetime(2018, 10, 20))
        self.assertIsNone(a.getDetails().get("tags", None))
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
            # 2c. WHAT is nonexistant => Action is None, error message present
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsNone(a)
        self.assertGreater(len(err), 0)
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
        # 3. ROOT enter verb synonym
            # 3a. WHAT feedback synonym => Set feedback for workout, no error msg
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.SetFeedbackAction)
        self.assertEqual(err, "")
        self.assertEqual(a.getDetails().get("time", None), datetime(2018, 11, 20))
        self.assertIsNone(a.getDetails().get("tags", None))
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
            # 3b. WHAT calories synonym => Set calories for workout, no error msg
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.SetCaloriesAction)
        self.assertEqual(err, "")
        self.assertEqual(a.getDetails().get("time", None), datetime(2018, 11, 20))
        self.assertIsNone(a.getDetails().get("tags", None))
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
            # 3c. WHAT is nonexistant => Action is None, error message present
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsNone(a)
        self.assertGreater(len(err), 0)
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
        # 4. ROOT help verb synonym => Help Action, no error msg
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsInstance(a, act.HelpAction)
        self.assertEqual(err, "")
        self.assertIsNone(a.getDetails().get("time", None))
        self.assertIsNone(a.getDetails().get("tags", None))
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()
        # 5-6. No ROOT or ROOT something random => Action is None, error message present
        a, err = self.ttac.tokens_to_action(self.tl1)
        self.assertIsNone(a)
        self.assertGreater(len(err), 0)
        self.ttac.initially_process_toks.assert_called_once_with(self.tl1)
        self.ttac.initially_process_toks.reset_mock()

    def tearDown(self):
        self.ttac = None