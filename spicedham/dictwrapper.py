from spicedham.backend import BaseBackend

class DictWrapper(BaseBackend):
    """
    A stupid simple in memory datastore using a dictionary.
    """

    store = {}

    def set_key(self, classifier, key, value):
        self.store[classifier + key] = value

    def get_key(self, classifier, key, default=None):
        return self.store.get(classifier + key, default)

    def reset(self):
        self.store = {}
