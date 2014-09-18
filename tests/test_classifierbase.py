from itertools import izip, cycle

from unittest import TestCase


class TestClassifierBase(TestCase):

    def _training(self, classification_type, classifier, alphabet,
                  reversed_alphabet):
        reversed_alphabet = reversed(alphabet)
        messagePairs = izip(alphabet, reversed_alphabet)
        for message, is_spam in izip(messagePairs, cycle((True, False))):
            classifier.train(classification_type, message, is_spam)
