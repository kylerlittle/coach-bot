import unittest
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime
from pytz import timezone
import importlib
nlp = importlib.import_module("coach-bot.nlp.tokens_to_action")

class MockToken(object):
    """Mock spaCy's Token Class, at least in terms of how it's
    used in TokensToActionConverter class.
    """
    def __init__(self, text, dep, lemma):
        self._text = text
        self._dep = dep
        self._lemma = lemma
    
    @property
    def text(self):
        return self._text

    @property
    def dep_(self):
        return self._dep

    @property
    def lemma_(self):
        return self._lemma

# ROOT MockTokens
sched_root = [MockToken('schedule', 'ROOT', 'schedule'), MockToken('plan', 'ROOT', 'request'), 
              MockToken('schedule', 'ROOT', 'request'), MockToken('fdslkfsjldf', 'ROOT', 'fdslkfsjldf')]


class TestTokensToAction(unittest.TestCase):
    def setUp(self):
        # Construct an instance of TokensToActionConverter
        self.ttac = nlp.TokensToActionConverter()
        # Make test token lists here.
        self.tl1 = []
        self.tl2 = [MockToken('5 PM', 'TIME', '5 PM'), MockToken('tomorrow', 'TIME', 'tomorrow')]          # TIME only
        self.tl3 = [MockToken('schedule', 'ROOT', 'schedule'), MockToken('workout', 'WHAT', 'workout')] # all not TIME
        self.tl4 = self.tl3 + self.tl2   # Mixture of TIME and not TIME

    def test_process_input(self):
        """Test process_input, which can either raise an InputError or return an action
        """
        # Stub return values for tokens_to_action.
        self.ttac.tokens_to_action = Mock(side_effect=[(None, "anything"), ("whatever", "anything")])
        self.assertRaises(nlp.InputError, self.ttac.process_input, self.tl1)           # assert
        self.ttac.tokens_to_action.assert_called_with(self.tl1)                        # verify
        self.assertEqual(self.ttac.process_input(["hi"]), "whatever")            # assert whatever is returned is same as stub[0]
        self.ttac.tokens_to_action.assert_called_with(["hi"])                    # verify

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
        self.assertEqual(self.ttac.get_time_str(self.tl2), "5 PM tomorrow")
    
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
        self.ttac.get_time_toks = Mock(return_value=self.tl2)
        self.ttac.get_time_str = Mock(return_value="5 PM tomorrow")
        self.ttac.get_datetime_from_str = Mock(return_value=datetime(2018, 10, 5))
        self.assertEquals(self.ttac.get_datetime_from_tok_list(self.tl1), datetime(2018, 10, 5))
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
        # List with no ATTRIBUTE dep's
        # List with some ATTRIBUTE dep's
        # List with all ATTRIBUTE dep's
        pass

    def test_initially_process_toks(self):
        # Four mocks
        # One test
        # Four verifications
        pass

    def test_tokens_to_action(self):
        # Need several mocks for self.ttac.initially_process_toks
        # 1. ROOT schedule verb synonym
        # 2. ROOT display verb synonym
            # 2a. WHAT schedule noun synonym
                # 2a i. ATTRIBUTE workout synonym
                # 2a ii. ATTRIBUTE present but no workout synonym
                # 2a iii. NO ATTRIBUTE
            # 2b. WHAT statistics synonym
            # 2c-d. WHAT is nonexistant or something random
        # 3. ROOT enter verb synonym
            # 3a. WHAT feedback synonym
            # 3b. WHAT calories synonym
            # 3c-d. WHAT is nonexistant or something random
        # 4. ROOT help verb synonym
        # 5-6. No ROOT or ROOT something random

        # VERIFICATIONS!
        pass

    def tearDown(self):
        self.ttac = None