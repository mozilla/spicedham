# -*- coding: utf-8 -*-
from __future__ import division
import re
import json

from spicedham import backend

def foo():
    print 'rest'

class Bayes(object):

    def setup(self):
        backend.setup()

    def train(self, result, is_spam):
        """Train the database on result. result is a dict, is_spam is a bool"""
        print 'training'
        total = backend.get_key('*', {'numSpam': 0, 'numTotal': 0})
        results = set(result)
        for item in results:
            total['numTotal'] += 1
            if is_spam:
                total['numSpam'] += 1
            item = _train_single(item, is_spam)
        backend.set_key_list(results)


    def _train_single(item, is_spam):
        value = backend.get_key(item)
        if not value:
            value = Store()
            value['numTotal'] = 0
            value['numSpam'] = 0
        value['numTotal'] += 1
        if is_spam:
            value['numSpam'] += 1
        return value

    def classify(self, response):
        """Get the probability that a response is spam. response is a list"""
        total = backend.get_key('*')
        pSpam = float(total.numSpam) / float(total.numTotal)
        # Since spam and ham are independant events
        pHam = 1.0 - pSpam
        pSpamGivenWord = pSpam
        pHamGivenWord = pHam
        pWordList = []
        for description in set(response):
            if description == '*' or description == '':
                continue
            word = backend.get_key(description, {'numTotal': 0, 'numSpam': 0})
            pWord = word.numTotal / total.numTotal
            pWordGivenSpam = word.numSpam / total.numSpam
            pWordGivenHam = word.numTotal - word.numSpam / total.numTotal - total.numSpam
            pSpamGivenWord *= pWordGivenSpam / pWord
            pHamGivenWord *= pWordGivenHam / pWord

        p = pSpamGivenWord / (pSpamGivenWord + pHamGivenWord)
        return p
