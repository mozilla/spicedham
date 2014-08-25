import operator
from itertools import imap, repeat

from spicedham.config import config
from spicedham.backend import Backend
from spicedham.baseplugin import BasePlugin

class NonsenseFilter(BasePlugin):
    """
    Filter messages with no words in the database.
    """

    def __init__(self):
        """
        Get values from the config.
        """
        self.filter_match = config['nonsensefilter']['filter_match']
        self.filter_miss = config['nonsensefilter']['filter_miss']
    
    # TODO: This is a lie, training is necessary, just not besides the 
    # training provided by the bayesian classifier.
    def train(self, tag, response, value):
        """
        No training necessary.
        """
        pass

    # TODO: Will match responses consisting of only ''
    def classify(self, tag, response):
        """
        If the message contains only words not found in the database return
        filter_match. Else return filter_miss.
        """
        list_in_dict = lambda x, y: not Backend.get_key(x, y, False)
        if all(imap(list_in_dict, repeat(tag), response)):
            return self.filter_match
        else:
            return self.filter_miss
