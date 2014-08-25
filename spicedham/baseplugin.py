class BasePlugin(object):
    """
    A base class for spicedham plugins.
    """

    def train(self, tag, result, is_spam):
       """
       Train the classifier on a single iterable piece of data called
       `result`.
       `tag` is a string tag which will be part of the compound key
       identifying the data.
       `is_spam` is a boolean indicating whether the result should be
       considered spam.
       """
       pass


    def classify(self, result):
        """
        Takes an iterable `result` and returns the probability that it
        is spam."""
        pass
