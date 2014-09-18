from unittest import TestCase

from nose.exc import SkipTest

from spicedham.dictwrapper import DictWrapper


try:
    from spicedham.sqlalchemywrapper import SqlAlchemyWrapper
except ImportError:
    pass


try:
    from spicedham.rediswrapper import RedisWrapper
except ImportError:
    pass


class TestRedisWrapperAPIConformation(TestCase):

    def setUp(self):
        try:
            import redis
            try:
                # Open a connection and check that there's a reachable
                # redis server on localhost
                r = redis.Redis()
                r.ping()
            except redis.ConnectionError:
                raise SkipTest('No Redis server on localhost')
        except ImportError:
            raise SkipTest('Redis not installed')

    def test_reset(self):
        r = RedisWrapper({})
        _test_subclass_reset(r)

    def test_set_and_get(self):
        r = RedisWrapper({})
        _test_subclass_set_and_get(r)

    def test_set_list_and_get_list(self):
        r = RedisWrapper({})
        _test_subclass_set_list_and_get_list(r)


class TestSqlAlchemyWrapperAPIConformation(TestCase):

    def setUp(self):
        try:
            import sqlalchemy  # noqa
        except ImportError:
            raise SkipTest('SqlAlchemy not installed')

    def test_reset(self):
        r = SqlAlchemyWrapper({})
        _test_subclass_reset(r)

    def test_set_and_get(self):
        r = SqlAlchemyWrapper({})
        _test_subclass_set_and_get(r)

    def test_set_list_and_get_list(self):
        r = SqlAlchemyWrapper({})
        _test_subclass_set_list_and_get_list(r)


class TestDictWrapperAPIConformation(TestCase):

    def test_reset(self):
        r = DictWrapper({})
        _test_subclass_reset(r)

    def test_set_and_get(self):
        r = DictWrapper({})
        _test_subclass_set_and_get(r)

    def test_set_list_and_get_list(self):
        r = DictWrapper({})
        _test_subclass_set_list_and_get_list(r)


def _test_subclass_reset(subclass):
    key0 = 'key0'
    value0 = {'val': 0}
    classifier = 'classifier'
    classification_type = 'type'
    subclass.set_key(classification_type, classifier, key0, value0)
    subclass.reset()
    received_value0 = subclass.get_key(classification_type, classifier, key0)
    assert received_value0 is None


def _test_subclass_set_and_get(subclass):
    subclass.reset()
    classifier = 'classifier'
    classification_type = 'type'
    key0 = 'key0'
    key1 = 'key1'
    key2 = 'key2'
    value0 = {'val': 0}
    value1 = {'val': 1}
    value2 = {'val': 2}
    subclass.set_key(classification_type, classifier, key0, value0)
    received_value0 = subclass.get_key(classification_type, classifier, key0)
    subclass.set_key(classification_type, classifier, key1, value1)
    received_value1 = subclass.get_key(classification_type, classifier, key1)
    subclass.set_key(classification_type, classifier, key2, value2)
    received_value2 = subclass.get_key(classification_type, classifier, key2)
    assert received_value0 == value0
    assert received_value1 == value1
    assert received_value2 == value2
    received_value3 = subclass.get_key(classification_type, classifier,
                                       'not_set')
    assert received_value3 is None
    received_value4 = subclass.get_key(classification_type, classifier,
                                       'not_set', 'default')
    assert received_value4 == 'default'


def _test_subclass_set_list_and_get_list(subclass):
    subclass.reset()
    classifier = 'classifier'
    classification_type = 'type'
    key0 = 'key0'
    key1 = 'key1'
    key2 = 'key2'
    value0 = {'val': 0}
    value1 = {'val': 1}
    value2 = {'val': 2}
    set_list = [(key0, value0), (key1, value1), (key2, value2)]
    get_list = [key0, key1, key2, 'not_set']
    expected_list = [value0, value1, value2, None]
    subclass.set_key_list(classification_type, classifier, set_list)
    received_list = subclass.get_key_list(classification_type, classifier,
                                          get_list)
    print received_list, get_list, subclass
    assert sorted(expected_list) == sorted(received_list)
