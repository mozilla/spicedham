import operator
from itertools import imap
from spicedham.backend import Backend

class NonsenseFilter(object):
    
    def train(self, response, value):
        pass

    def classify(self, response):
        list_in_dict = lambda x: not Backend.get_key(x, {'numTotal': 0, 'numSpam': False})
        if all(imap(list_in_dict, response)):
            return .7
        else:
            return None

