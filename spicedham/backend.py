from itertools import izip, repeat


class BaseBackend(object):
    """
    A base class for backend plugins.
    """

    def __init__(self, config):
        pass

    def reset(self):
        """
        Resets the training data to a blank slate.
        """
        raise NotImplementedError()


    def get_key(self, classification_type, classifier, key, default=None):
        """
        Gets the value held by the classifier, key composite key.
        If it doesn't exist, return default.
        """
        raise NotImplementedError()

    def get_key_list(self, classification_type, classifier, keys, default=None):
        """
        Given a list of key, classifier pairs get all values.
        If key, classifier doesn't exist, return default.
        Subclasses can override this to make more efficient queries for bulk
        requests.
        """
        return [self.get_key(classification_type, classifier, key, default)
                for key in keys]

    def set_key(self, classification_type, classifier, key, value):
        """
        Set the value held by the classifier, key composite key.
        """
        raise NotImplementedError()

    def set_key_list(self, classification_type, classifier, key_value_pairs):
        """
        Given a list of pairs of key, value  and a classifier set them all.
        Subclasses can override this to make more efficient queries for bulk
        requests.
        """
        return [self.set_key(classification_type, classifier, key, value)
                for key, value
                in key_value_pairs]
