from spicedham.basewrapper import BaseWrapper

class DigitDestroyer(BaseWrapper):
    def train(*args):
        pass
    def classify(self, response):
        if all(map(unicode.isdigit, response)):
            return 1
        else:
            return 0.5
