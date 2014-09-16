import json
from unittest import TestCase

from spicedham.sqlalchemywrapper import SqlAlchemyWrapper, EngineNotFoundError
from spicedham.sqlalchemywrapper.models import Store


class TestSqlAlchemyWrapper(TestCase):

    def test_no_config(self):
        """
        Making a new SqlAlchemyWrapper without specifying a backend should
        raise an EngineNotFoundError.
        """
        self.assertRaises(EngineNotFoundError, SqlAlchemyWrapper, {})

    def test_reset(self):
        sqlalchemy = SqlAlchemyWrapper({'engine': 'sqlite:///:memory:'})
        session = sqlalchemy.sessionFactory()
        test_store = Store()
        test_store.key = 'key'
        test_store.value = 'value'
        test_store.classifier = 'classifier'
        session.add(test_store)
        session.commit()
        sqlalchemy.reset()
        session = sqlalchemy.sessionFactory()
        self.assertTrue(len(session.query(Store).all()) == 0)

    def test_set_key(self):
        sqlalchemy = SqlAlchemyWrapper({'engine': 'sqlite:///:memory:'})
        key = 'key'
        value = {'value': 0}
        s_value = json.dumps(value)
        classifier = 'classifier'
        # test setting a value
        sqlalchemy.set_key(classifier, key, value)
        session = sqlalchemy.sessionFactory()
        all_of_em = session.query(Store).all()
        session.close()
        self.assertTrue(len(all_of_em) == 1)
        self.assertTrue(all_of_em[0].value == s_value)
        self.assertTrue(all_of_em[0].key == key)
        self.assertTrue(all_of_em[0].classifier == classifier)

        # test changing a value
        all_of_em = session.query(Store).all()
        self.assertTrue(len(all_of_em) == 1)
        d_value_new = {'value': 1, 'newkey': 0}
        value_new = json.dumps(d_value_new)
        sqlalchemy.set_key(classifier, key, d_value_new)
        session = sqlalchemy.sessionFactory()
        all_of_em = session.query(Store).all()
        session.close()
        self.assertTrue(len(all_of_em) == 1)
        self.assertTrue(all_of_em[0].value == unicode(value_new))
        self.assertTrue(all_of_em[0].key == key)
        self.assertTrue(all_of_em[0].classifier == classifier)

    def test_get_key(self):
        sqlalchemy = SqlAlchemyWrapper({'engine': 'sqlite:///:memory:'})
        key = 'key'
        value = {'value': 0}
        classifier = 'classifier'
        # Test when there is no value in the Store and no default
        result = sqlalchemy.get_key(classifier, key)
        self.assertTrue(result is None)
        # Test when there is no value in the Store and default is specified
        result = sqlalchemy.get_key(classifier, key, 1)
        self.assertTrue(result == 1)
        # Test when there is a value in the Store
        sqlalchemy.set_key(classifier, key, value)
        result = sqlalchemy.get_key(classifier, key)
        self.assertEqual(result, value)

    def test_set_key_list(self):
        sqlalchemy = SqlAlchemyWrapper({'engine': 'sqlite:///:memory:'})
        key1 = 'key1'
        value1 = {'value1': 1}
        key2 = 'key2'
        value2 = {'value2': 2}
        classifier = 'classifier'
        key_val_list = [(key1, value1), (key2, value2)]
        sqlalchemy.set_key_list(classifier, key_val_list)
        value = sqlalchemy.get_key(classifier, key1)
        self.assertTrue(value == value1)
        value = sqlalchemy.get_key(classifier, key2)
        self.assertTrue(value == value2)

    def test_get_key_list(self):
        sqlalchemy = SqlAlchemyWrapper({'engine': 'sqlite:///:memory:'})
        key1 = 'key1'
        value1 = {'value1': 1}
        key2 = 'key2'
        value2 = {'value2': 2}
        classifier = 'classifier'
        key_val_list = [(key1, value1), (key2, value2)]
        sqlalchemy.set_key_list(classifier, key_val_list)
        values = sqlalchemy.get_key_list(classifier, [key1, key2])
        expected_values = [value1, value2]
        self.assertEqual(sorted(expected_values), sorted(values))
