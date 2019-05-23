import unittest
from wkdict.wkdict import parseJSON
from wkdict.wkdict import requestAPI

class TestWkdict(unittest.TestCase):
    def test_good_inputs(self):
        raised = False
        try:
            words = ["If", "there", "a", "main", "concern", "Google",
                     "may", "have", "oversold"]
            for word in words:
                word, resjson = requestAPI(word)
                ret = parseJSON(word, resjson, 1)
        except:
            raised = True
        self.assertFalse(raised)

    def test_bad_inputs(self):
        raised = False
        try:
            words = [".", "?", "(Google)",
                     "ma$y", "ha^ve"]
            for word in words:
                word, resjson = requestAPI(word)
                ret = parseJSON(word, resjson, 1)
                self.assertTrue("The word you typed is" in ret)
        except:
            raised = True
        self.assertFalse(raised)