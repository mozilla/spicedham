from unittest import TestCase
from itertools import repeat, imap, izip, cycle

from spicedham.bayes import Bayes
from spicedham.backend import load_backend


class TestBayes(TestCase):
    
    def test_classify(self):
        Backend = load_backend()
        Backend.reset(True)
        b = Bayes()
        self._training(b)
        alphabet = map(chr, range(97, 123))
        for letter in alphabet:
            p = b.classify('tag', letter)
            self.assertEqual(p, 0.5)

    def _training(self, bayes):
        tag = 'tag'
        alphabet = map(chr, range(97, 123))
        reversed_alphabet = reversed(alphabet)
        messagePairs = izip(alphabet, reversed_alphabet)
        for tag, message, is_spam in izip(repeat(tag), messagePairs, cycle((True, False))):
            bayes.train(tag, message, is_spam)

        

    def test_train(self):
        Backend = load_backend()
        Backend.reset(True)
        alphabet = map(chr, range(97, 123))
        b = Bayes()
        self._training(b)
        for letter in alphabet:
            result = Backend.get_key('tag', letter)
            self.assertEqual(result, {'numTotal': 2, 'numSpam': 1})
            self.assertGreaterEqual(result['numTotal'], result['numSpam'])
