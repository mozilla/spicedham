from spicedham.backend import BaseBackend

class DictWrapper(BaseBackend):

    store = {}

    def set_key(self, classifier, key, value):
        """
        Classifier and key are strings. value may be anything.
        """
        self.store[classifier + key] = value

    def get_key(self, classifier, key, default=None):
        """
        Classifier and key are strings. returned value may be anything.
        """
        return self.store.get(classifier + key, default)

    def reset(self):
        """
        Removes everything from the backend.
        """
        self.store = {}
