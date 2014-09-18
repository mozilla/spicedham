# -*- coding: utf-8 -*-
# python 3 style division avoids the need to cast to floats
# absolutely everywhere
from __future__ import division
import logging


from spicedham.plugin import BasePlugin


class NotYetTrainedError(Exception):
    """
    Raise this error if a classifier's classify method is called but is has not
    yet been trained.
    """
    pass


log = logging.getLogger('spicedham')


class Bayes(BasePlugin):
    """
    A Bayesian classifier plugin
    """

    def __init__(self, config, backend):
        self.backend = backend

    def train(self, classification_type,  result, is_spam):
        """
        Train the database on result. result is a dict, is_spam is a bool
        """
        # * is a special key representing all results. This is kind of a hack.
        total = self.backend.get_key(classification_type,
                                     self.__class__.__name__,'*',
                                     {'numSpam': 0, 'numTotal': 0})
        results = []
        for item in set(result):
            value = self.backend.get_key(classification_type,
                                         self.__class__.__name__, item,
                                         {'numSpam': 0, 'numTotal': 0})
            total['numTotal'] += 1
            value['numTotal'] += 1
            if is_spam:
                total['numSpam'] += 1
                value['numSpam'] += 1
            results.append((item, value))
        self.backend.set_key_list(classification_type,
                                  self.__class__.__name__, results)
        self.backend.set_key(classification_type, self.__class__.__name__,
                             '*', total)

    def explain(self, classification_type, response):
        """
        Get the probability that a response is spam, and a unicode explanation
        for the probability. response is a list.
        Raise NotYetTrainedError if the classifier has not yet been trained.
        """
        total = self.backend.get_key(self.__class__.__name__, '*')
        if total is None:
            raise NotYetTrainedError()
        pSpam = total['numSpam'] / total['numTotal']
        # Since spam and ham are independant events
        pHam = 1.0 - pSpam
        pSpamGivenWord = pSpam
        pHamGivenWord = pHam
        explanation = ''
        for description in set(response):
            # ignore reserved '*' or useless ''
            if description == '*' or description == '':
                continue
            word = self.backend.get_key(classification_type,
                                        self.__class__.__name__, description,
                                        {'numTotal': 0, 'numSpam': 0})
            # If there's no data on the word, ignore it
            if word['numTotal'] == 0 or word['numSpam'] == 0:
                continue
            # TODO: make an exception, not just an assert
            assert word['numTotal'] >= word['numSpam']
            pWord = (word['numTotal'] / total['numTotal'])
            pWordGivenSpam = (word['numSpam']) / total['numSpam']
            pWordGivenHam = ((word['numTotal'] - word['numSpam']) /
                             (total['numTotal'] - total['numSpam']))
            pSpamGivenWord *= (pWordGivenSpam) / pWord
            pHamGivenWord *= pWordGivenHam / pWord
            explanation += u' word: {0} prob word: {1} prob spam: {2} prob spam: \
                {3}'.format(unicode(description), unicode(pWord),
                            unicode(pWordGivenSpam), unicode(pWordGivenHam),
                            unicode(pWordGivenSpam/pWord),
                            unicode(pWordGivenHam/pWord))
        log.debug(explanation)

        p = ((pSpamGivenWord) / (pSpamGivenWord + pHamGivenWord))
        return (p, explanation)
