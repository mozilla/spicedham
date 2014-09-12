# -*- coding: utf-8 -*-
# python 3 style division avoids the need to cast to floats
# absolutely everywhere
from __future__ import division
import re
import json
import logging



from spicedham.plugin import BasePlugin


class NotYetTrainedError(Exception):
    """
    Raise this error if a classifier's classify method is called but is has not
    yet been trained.
    """
    pass


class Bayes(BasePlugin):
    """
    A Bayesian classifier plugin
    """

    def __init__(self, config, backend):
        self.backend = backend
        logging.basicConfig(filename='sh_bayes_classifier.log',
                            level=logging.DEBUG)

    def train(self, result, is_spam):
        """
        Train the database on result. result is a dict, is_spam is a bool
        """
        # * is a special key representing all results. This is kind of a hack.
        total = self.backend.get_key(self.__class__.__name__,
            '*', {'numSpam': 0, 'numTotal': 0})
        results = []
        for item in set(result):
            value = self.backend.get_key(self.__class__.__name__, item,
                {'numSpam': 0, 'numTotal': 0})
            total['numTotal'] += 1
            value['numTotal'] += 1
            if is_spam:
                total['numSpam'] += 1
                value['numSpam'] += 1
            results.append((item, value))
        self.backend.set_key_list(self.__class__.__name__, results)
        self.backend.set_key(self.__class__.__name__, '*', total)

    def classify(self, response):
        """
        Get the probability that a response is spam. response is a list.
        Raise NotYetTrainedError if the classifier has not yet been trained.
        """
        total = self.backend.get_key(self.__class__.__name__, '*')
        if total == None:
            raise NotYetTrainedError()
        pSpam = total['numSpam'] / total['numTotal']
        # Since spam and ham are independant events
        pHam = 1.0 - pSpam
        pSpamGivenWord = pSpam
        pHamGivenWord = pHam
        logging_message = ''
        pWordList = []
        for description in set(response):
            # ignore reserved '*' or useless ''
            if description == '*' or description == '':
                continue
            word = self.backend.get_key(self.__class__.__name__, description,
                {'numTotal': 0, 'numSpam': 0})
            # If there's no data on the word, ignore it
            if word['numTotal'] == 0 or  word['numSpam'] == 0:
                continue
            # TODO: make an exception, not just an assert
            assert word['numTotal'] >= word['numSpam']
            logging_message += 'The word is: ' + description
            pWord = (word['numTotal'] / total['numTotal'])
            logging_message += ' The probability of the word is: ' + str(pWord)
            pWordGivenSpam = (word['numSpam']) / total['numSpam']
            logging_message += ' The probability of the word given spam is ' + str(pWordGivenSpam)
            pWordGivenHam = (word['numTotal'] - word['numSpam']) / (total['numTotal'] - total['numSpam'])
            logging_message += ' The probability of the word given ham is ' + str(pWordGivenHam)
            pSpamGivenWord *= (pWordGivenSpam) / pWord
            logging_message += ' The probability of the spam given word is ' + str(pWordGivenSpam/pWord)
            pHamGivenWord *= pWordGivenHam / pWord
            logging_message += ' The probability of the ham given word is ' + str(pWordGivenHam/pWord)

        p = ((pSpamGivenWord) / (pSpamGivenWord + pHamGivenWord))
        if p > 0.5:
            logging.debug(logging_message)
        return (p)
