import json
import redis
from spicedham.backend import BaseBackend

class RedisWrapper(BaseBackend):

    def __init__(self, config):
        """
        Connects to a redis server specified in the config, or defaults to
        a development server on localhost.
        """
        rediswrapper_config = config.get('rediswrapper', {})
        host = rediswrapper_config.get('host', 'localhost')
        port = rediswrapper_config.get('port', 6379)
        db = rediswrapper_config.get('db', 0)
        self.redis_server = redis.StrictRedis(host=host, port=port, db=db)

    def set_key(self, classifier, key, value):
        """
        classifier and key are strings which will be concatenated to form a
        simgle key. value is a jsonifiable dictionary.
        """
        value = json.dumps(value)
        self.redis_server.set(classifier + key, value)

    def get_key(self, classifier, key, default=None):
        """
        classifier and key are strings which will be concatenated to form a
        simgle key. The returned value is a dictionary.
        """
        value = self.redis_server.get(classifier + key)
        if value is None:
            return default
        return json.loads(value)

    def reset(self):
        """
        Drops all keys in the current redis database.
        """
        self.redis_server.flushdb()
