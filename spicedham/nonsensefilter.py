import operator
from itertools import imap, repeat

from spicedham.config import config
from spicedham.backend import Backend
from spicedham.baseplugin import BasePlugin

class NonsenseFilter(BasePlugin):

    def __init__(self):
        self.filter_match = config['nonsensefilter']['filter_match']
        self.filter_miss = config['nonsensefilter']['filter_miss']
    
    def train(self, tag, response, value):
        pass

    def classify(self, tag, response):
        list_in_dict = lambda x, y: not Backend.get_key(x, y, False)
        if all(imap(list_in_dict, repeat(tag), response)):
            return self.filter_match
        else:
            return self.filter_miss
