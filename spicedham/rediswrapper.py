import json
from hashlib import md5

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

    def gen_hash(self, classifier, key):
        key_hash = md5(key).hexdigest()
        classifier_hash = md5(classifier).hexdigest()
        return classifier_hash + '::' + key_hash

    def set_key(self, classifier, key, value):
        value = json.dumps(value)
        self.redis_server.set(self.gen_hash(classifier, key), value)

    def get_key(self, classifier, key, default=None):
        value = self.redis_server.get(self.gen_hash(classifier, key))
        if value is None:
            return default
        return json.loads(value)

    def reset(self):
        self.redis_server.flushdb()
