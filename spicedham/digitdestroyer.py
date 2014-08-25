from itertools import repeat
from spicedham.basewrapper import BaseWrapper
from spicedham.config import load_config
from spicedham.baseplugin import BasePlugin

class DigitDestroyer(BasePlugin):
    """
    Filter all responses which consist of only numbers and no words.
    """

    def __init__(self):
        """
        Get values from the config.
        """
        config = load_config()
        self.filter_match = config['digitdestroyer']['filter_match']
        self.filter_miss = config['digitdestroyer']['filter_miss']

    def train(*args):
        """
        There is no training necessary.
        """
        pass

    def classify(self, tag, response):
        """
        If the responses consists entirely of numbers, return the filter_match
        value from the config file. Otherwise return filter_miss.
        """
        if all(map(unicode.isdigit, unicode(response))):
            return self.filter_match
        else:
            return self.filter_miss
