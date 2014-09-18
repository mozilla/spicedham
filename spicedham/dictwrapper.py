from spicedham.backend import BaseBackend


class DictWrapper(BaseBackend):
    """
    A stupid simple in memory datastore using a dictionary.
    """

    store = {}

    def set_key(self, classification_type, classifier, key, value):
        self.store[(classification_type, classifier, key)] = value

    def get_key(self, classification_type,  classifier, key, default=None):
        return self.store.get((classification_type, classifier, key), default)

    def reset(self):
        self.store = {}
