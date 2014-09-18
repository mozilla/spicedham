from unittest import TestCase

from spicedham import Spicedham
from spicedham.digitdestroyer import DigitDestroyer


class TestDigitDestroyer(TestCase):

    def test_classify(self):
        classifier_type = 'type'
        sh = Spicedham()
        dd = DigitDestroyer(sh.config, sh.backend)
        dd.filter_match = 1
        dd.filter_miss = 0
        match_message = ['1', '2', '3', '1', '1']
        miss_message = ['a', '100']
        self.assertEqual(dd.classify(classifier_type, match_message), 1)
        self.assertEqual(dd.classify(classifier_type, miss_message), 0)

    def test_explain(self):
        classifier_type = 'type'
        sh = Spicedham()
        dd = DigitDestroyer(sh.config, sh.backend)
        dd.filter_match = 1
        dd.filter_miss = 0
        match_message = ['1', '2', '3', '1', '1']
        miss_message = ['a', '100']
        value_match, explanation = dd.explain(classifier_type, match_message)
        self.assertEqual(value_match, 1)
        self.assertEqual(type(explanation), str)
        value_miss, explanation = dd.explain(classifier_type, miss_message)
        self.assertEqual(value_miss, 0)
        self.assertEqual(type(explanation), str)
