from itertools import izip, cycle

from unittest import TestCase

from spicedham import Spicedham

class SpicedhamTestCase(TestCase):

    def setUp(self):
        self.sh = Spicedham({'backend': 'SqlAlchemyWrapper',
                             'engine': 'sqlite:///:memory:',
                             'tokenizer': 'SplitTokenizer'})

    def _training(self, classification_type, classifier, alphabet,
                  reversed_alphabet):
        reversed_alphabet = reversed(alphabet)
        messagePairs = izip(alphabet, reversed_alphabet)
        for message, is_spam in izip(messagePairs, cycle((True, False))):
            classifier.train(classification_type, message, is_spam)
