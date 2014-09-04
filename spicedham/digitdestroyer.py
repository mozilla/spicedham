from itertools import repeat
from spicedham.basewrapper import BaseWrapper
from spicedham.baseplugin import BasePlugin

class DigitDestroyer(BasePlugin):
    """
    Filter all responses which consist of only numbers and no words.
    """

    def __init__(self, spiced_ham):
        """
        Get values from the config.
        """
        digitdestroyer_config = spiced_ham.config.get('digitdestroyer', {})
        self.filter_match = digitdestroyer_config.get('filter_match', 1)
        self.filter_miss = digitdestroyer_config.get('filter_miss', None)

    def train(*args):
        """
        There is no training necessary.
        """
        pass

    def classify(self, response):
        """
        If the responses consists entirely of numbers, return the filter_match
        value from the config file. Otherwise return filter_miss.
        """
        if all(map(unicode.isdigit, map(unicode, response))):
            return self.filter_match
        else:
            return self.filter_miss
