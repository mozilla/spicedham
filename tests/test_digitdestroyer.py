from unittest import TestCase

from spicedham.digitdestroyer import DigitDestroyer

class TestDigitDestroyer(TestCase):
    
    def test_classify(self):
        dd = DigitDestroyer()
        dd.filter_match = 1
        dd.filter_miss = 0
        match_message = ['1', '2', '3', '1', '1']
        miss_message = ['a', '100']
        self.assertEqual(dd.classify(match_message), 1)
        self.assertEqual(dd.classify(miss_message), 0)

