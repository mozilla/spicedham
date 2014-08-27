
class BaseWrapper(object):
    """
    A base class for backend plugins.
    """

    def reset(self, really):
        """
        Resets the training data to a blank slate.
        """
        if really:
            raise NotImplementedError()


    def get_key(self, tag, key, default=None):
        """
        Gets the value held by the tag, key composite key. If it doesn't exist,
        return default.
        """
        raise NotImplementedError()


    def get_key_list(self, tag, keys, default=None):
        """
        Given a list of key, tag tuples get all values.
        If key, tag doesn't exist, return default.
        Subclasses can override this to make more efficient queries for bulk
        requests.
        """
        return [self.get_key(tag, key, default) for tag, key in key_tag_pairs]


    def set_key_list(self, tag_key_value_tuples):
        """
        Given a list of tuples of tag, key, value set them all.
        Subclasses can override this to make more efficient queries for bulk
        requests.
        """
        return [self.set_key(tag, key, value) for tag, key, value in tag_key_value_tuples]


    def set_key(self, tag, key, value):
        """
        Set the value held by the tag, key composite key.
        """
        raise NotImplementedError()
