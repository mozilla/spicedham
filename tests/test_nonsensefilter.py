from tests.test_classifierbase import TestClassifierBase

from spicedham.nonsensefilter import NonsenseFilter
from spicedham import Spicedham

class TestNonsenseFilter(TestClassifierBase):

    def test_train(self):
        sh = Spicedham()
        nonsense = NonsenseFilter(sh)
        alphabet = map(chr, range(97, 123))
        reversed_alphabet = reversed(alphabet)
        self._training(nonsense, alphabet, reversed_alphabet)
        for letter in alphabet:
            self.assertEqual(True,
                sh.backend.get_key(nonsense.__class__.__name__, letter))
    
    def test_classify(self):
        sh = Spicedham()
        nonsense = NonsenseFilter(sh)
        nonsense.filter_match = 1
        nonsense.filter_miss = 0
        alphabet = map(chr, range(97, 123))
        reversed_alphabet = reversed(alphabet)
        self._training(nonsense, alphabet, reversed_alphabet)
        match_message = ['not', 'in', 'training', 'set']
        miss_message = ['a']
        self.assertEqual(nonsense.classify(match_message), 1)
        self.assertEqual(nonsense.classify(miss_message), 0)
