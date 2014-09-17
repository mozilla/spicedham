from unittest import TestCase

from spicedham import Spicedham
from spicedham.backend import BaseBackend
from spicedham.dictwrapper import DictWrapper
try:
    from spicedham.sqlalchemywrapper import SqlAlchemyWrapper
except ImportError as e:
    print 'SqlAlchemy was not installed. Will not test SqlAlchemyWrapper'    


try:
    from spicedham.rediswrapper import RedisWrapper
except ImportError as e:
    print 'Redis was not installed. Will not test RedisWrapper'    


def test_all_subclasses():
    sh = Spicedham()
    all_subclasses = sh.all_subclasses
    for subclass in all_subclasses(BaseBackend):
        sub_obj = subclass({'engine': 'sqlite:///./db.sqlite'})
        yield _test_subclass_reset, sub_obj
        yield _test_subclass_set_and_get, sub_obj
        yield _test_subclass_set_list_and_get_list, sub_obj

def _test_subclass_reset(subclass):
    key0 = 'key0'
    value0 = {'val': 0}
    classifier = 'classifier'
    subclass.set_key(classifier, key0, value0)
    subclass.reset()
    received_value0 = subclass.get_key(classifier, key0)
    assert received_value0 is None
    

def _test_subclass_set_and_get(subclass):
    subclass.reset()
    classifier = 'classifier'
    key0 = 'key0'
    key1 = 'key1'
    key2 = 'key2'
    value0 = {'val': 0}
    value1 = {'val': 1}
    value2 = {'val': 2}
    subclass.set_key(classifier, key0, value0)
    received_value0 = subclass.get_key(classifier, key0)
    subclass.set_key(classifier, key1, value1)
    received_value1 = subclass.get_key(classifier, key1)
    subclass.set_key(classifier, key2, value2)
    received_value2 = subclass.get_key(classifier, key2)
    assert received_value0 == value0
    assert received_value1 == value1
    assert received_value2 == value2
    received_value3 = subclass.get_key(classifier, 'not_set')
    assert received_value3 is None
    received_value4 = subclass.get_key(classifier, 'not_set', 'default')
    assert received_value4 == 'default'

def _test_subclass_set_list_and_get_list(subclass):
    subclass.reset()
    classifier = 'classifier'
    key0 = 'key0'
    key1 = 'key1'
    key2 = 'key2'
    value0 = {'val': 0}
    value1 = {'val': 1}
    value2 = {'val': 2}
    set_list = [(key0, value0), (key1, value1), (key2, value2)]
    get_list = [key0, key1, key2, 'not_set']
    expected_list = [value0, value1, value2, None]
    subclass.set_key_list(classifier, set_list)
    received_list = subclass.get_key_list(classifier, get_list)
    print received_list, get_list, subclass
    assert sorted(expected_list) == sorted(received_list)
