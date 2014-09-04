class BasePlugin(object):
    """
    A base class for spicedham plugins.
    """
    def __init__(self, spiced_ham_object):
        pass

    def train(self, result, is_spam):
       """
       Train the classifier on a single iterable piece of data called
       `result`.
       `is_spam` is a boolean indicating whether the result should be
       considered spam.
       """
       pass


    def classify(self, result):
        """
        Takes an iterable `result` and returns the probability that it
        is spam."""
        pass
