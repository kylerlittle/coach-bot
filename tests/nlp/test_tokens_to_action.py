import unittest
from unittest.mock import MagicMock, Mock
import importlib
nlp = importlib.import_module("coach-bot.nlp.tokens_to_action")
# nlp = __import__("coach-bot.nlp.tokens_to_action")  # import it this way since hyphenated

class MockToken(object):
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
        pass

    def test_process_input(self):
        # This method can either raise an InputError or return an action
        ttac = nlp.TokensToActionConverter()
        # Stub return value for tokens_to_action.
        ttac.tokens_to_action = Mock(side_effect=[(None, "anything"), ("whatever", "anything")])
        self.assertRaises(nlp.InputError, ttac.process_input, [])           # assert
        ttac.tokens_to_action.assert_called_with([])                        # verify
        self.assertEqual(ttac.process_input(["hi"]), "whatever")            # assert whatever is returned is same as stub[0]
        ttac.tokens_to_action.assert_called_with(["hi"])                    # verify

    def test_get_time_toks(self):
        pass

    def test_get_time_str(self):
        pass
    
    def test_get_datetime_from_str(self):
        pass

    def test_get_root_action(self):
        pass

    def test_get_action_receiver(self):
        pass

    def test_get_action_receiver_attrs(self):
        pass

    def test_initially_process_toks(self):
        pass

    def test_tokens_to_action(self):
        pass

    def tearDown(self):
        pass