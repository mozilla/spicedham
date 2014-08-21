from itertools import repeat
from spicedham.basewrapper import BaseWrapper
from spicedham.config import config

class DigitDestroyer(object):

    def __init__(self):
        self.filter_match = config['digitdestroyer']['filter_match']
        self.filter_miss = config['digitdestroyer']['filter_miss']

    def train(*args):
        pass
    def classify(self, tag, response):
        if all(map(unicode.isdigit, unicode(response))):
            return self.filter_match
        else:
            return self.filter_miss
