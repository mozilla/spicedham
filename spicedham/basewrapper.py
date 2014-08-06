
class BaseWrapper(object):

    def set_up():
        pass

    def get_key(key, default=None):
        raise NotImplementedError()

    def get_key_list(keys, default=None):
        return [ get_key(key, default) for key in keys ]

    def set_key_list(key_value_tuples):
        return [ set_key(key, value) for key, value in key_value_tuples ] 

    def set_key(key, value):
        raise NotImplementedError()
