
class BaseWrapper(object):

    def set_up(self):
        pass

    def get_key(self, tag, key, default=None):
        raise NotImplementedError()

    def get_key_list(self, tag, keys, default=None):
        return [ self.get_key(key, default) for key in keys ]

    def set_key_list(self, tag, key_value_tuples):
        return [ self.set_key(key, value) for key, value in key_value_tuples ]

    def set_key(self, tag, key, value):
        raise NotImplementedError()
