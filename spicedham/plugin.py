class BasePlugin(object):
    """
    A base class for spicedham plugins.
    """
    def __init__(self, config, backend):
        pass

    def train(self, result, is_spam):
        """
        Train the classifier on a single iterable piece of data called
        `result`.
        `is_spam` is a boolean indicating whether the result should be
        considered spam.
        """
        pass

    def classify(self, classification_type, result):
        """
        Takes an iterable `result` and returns the probability that it
        is spam."""
        return self.explain(classification_type, result)[0]

    def explain(self, classification_type, result):
        """
        Takes an iterable `result` and returns the probability that it
        is spam as well as a list of strings explaining the probability
        """
        pass
