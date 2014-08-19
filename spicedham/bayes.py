# -*- coding: utf-8 -*-
from __future__ import division
import re
import json
import q

from spicedham.backend import Backend

class Bayes(object):

    def setup(self):
        Backend.setup()

    def train(self, tag, result, is_spam):
        """Train the database on result. result is a dict, is_spam is a bool"""
        total = Backend.get_key(tag, '*', {'numSpam': 0, 'numTotal': 0})
        results = []
        for item in set(result):
            value = Backend.get_key(tag, item, {'numSpam': 0, 'numTotal': 0})
            total['numTotal'] += 1
            value['numTotal'] += 1
            if is_spam:
                total['numSpam'] += 1
                value['numSpam'] += 1
            results.append((item, value))
        Backend.set_key_list(tag, results)
        Backend.set_key(tag, '*', total)

    def classify(self, tag, response):
        """Get the probability that a response is spam. response is a list"""
        total = Backend.get_key(tag, '*')
        pSpam = total['numSpam'] / total['numTotal']
        # Since spam and ham are independant events
        q('CLASSIFY')
        pHam = 1.0 - pSpam
        pSpamGivenWord = pSpam
        pHamGivenWord = pHam
        pWordList = []
        for description in set(response):
            if description == '*' or description == '':
                continue
            word = Backend.get_key(tag, description, {'numTotal': 0, 'numSpam': 0})
            if word['numTotal'] == 0 or  word['numSpam'] == 0:
                continue
            q(description)
            assert word['numTotal'] >= word['numSpam']
            pWord = q(word['numTotal'] / total['numTotal'])
            pWordGivenSpam = (word['numSpam']) / total['numSpam']
            pWordGivenHam = (word['numTotal'] - word['numSpam']) / (total['numTotal'] - total['numSpam'])
            pSpamGivenWord *= (pWordGivenSpam) / pWord
            pHamGivenWord *= pWordGivenHam / pWord

        p = q((pSpamGivenWord) / (pSpamGivenWord + pHamGivenWord))
        if p > 0.5:
            q("SPAM")
        return (p)
