import json
from unittest import TestCase

from spicedham.sqlalchemywrapper import SqlAlchemyWrapper
from spicedham.sqlalchemywrapper.models import Store


class TestSqlAlchemyWrapper(TestCase):

    def setUp(self):
        self.sqlalchemy = SqlAlchemyWrapper({'engine': 'sqlite:///:memory:'})

    def test_reset(self):
        classifier_type = 'type'
        session = self.sqlalchemy.sessionFactory()
        test_store = Store()
        test_store.key = 'key'
        test_store.value = 'value'
        test_store.classifier = 'classifier'
        test_store.classification_type = classifier_type
        session.add(test_store)
        session.commit()
        self.sqlalchemy.reset()
        session = self.sqlalchemy.sessionFactory()
        self.assertTrue(len(session.query(Store).all()) == 0)

    def test_set_key(self):
        key = 'key'
        value = {'value': 0}
        s_value = json.dumps(value)
        classifier = 'classifier'
        classifier_type = 'type'
        # test setting a value
        self.sqlalchemy.set_key(classifier_type, classifier, key, value)
        session = self.sqlalchemy.sessionFactory()
        all_of_em = session.query(Store).all()
        session.close()
        self.assertTrue(len(all_of_em) == 1)
        self.assertTrue(all_of_em[0].value == s_value)
        self.assertTrue(all_of_em[0].key == key)
        self.assertTrue(all_of_em[0].classifier == classifier)
        self.assertTrue(all_of_em[0].classification_type == classifier_type)

        # test changing a value
        all_of_em = session.query(Store).all()
        self.assertTrue(len(all_of_em) == 1)
        d_value_new = {'value': 1, 'newkey': 0}
        value_new = json.dumps(d_value_new)
        self.sqlalchemy.set_key(classifier_type, classifier, key, d_value_new)
        session = self.sqlalchemy.sessionFactory()
        all_of_em = session.query(Store).all()
        session.close()
        self.assertTrue(len(all_of_em) == 1)
        self.assertTrue(all_of_em[0].value == unicode(value_new))
        self.assertTrue(all_of_em[0].key == key)
        self.assertTrue(all_of_em[0].classifier == classifier)
        self.assertTrue(all_of_em[0].classification_type == classifier_type)

    def test_get_key(self):
        classification_type = 'type'
        key = 'key'
        value = {'value': 0}
        classifier = 'classifier'
        # Test when there is no value in the Store and no default
        result = self.sqlalchemy.get_key(classification_type, classifier, key)
        self.assertTrue(result is None)
        # Test when there is no value in the Store and default is specified
        result = self.sqlalchemy.get_key(classification_type, classifier, key, 1)
        self.assertTrue(result == 1)
        # Test when there is a value in the Store
        self.sqlalchemy.set_key(classification_type, classifier, key, value)
        result = self.sqlalchemy.get_key(classification_type, classifier, key)
        self.assertEqual(result, value)

    def test_set_key_list(self):
        classification_type = 'type'
        key1 = 'key1'
        value1 = {'value1': 1}
        key2 = 'key2'
        value2 = {'value2': 2}
        classifier = 'classifier'
        key_val_list = [(key1, value1), (key2, value2)]
        self.sqlalchemy.set_key_list(classification_type, classifier, key_val_list)
        value = self.sqlalchemy.get_key(classification_type, classifier, key1)
        self.assertTrue(value == value1)
        value = self.sqlalchemy.get_key(classification_type, classifier, key2)
        self.assertTrue(value == value2)

    def test_get_key_list(self):
        classification_type = 'type'
        key1 = 'key1'
        value1 = {'value1': 1}
        key2 = 'key2'
        value2 = {'value2': 2}
        classifier = 'classifier'
        key_val_list = [(key1, value1), (key2, value2)]
        self.sqlalchemy.set_key_list(classification_type, classifier, key_val_list)
        values = self.sqlalchemy.get_key_list(classification_type, classifier, [key1, key2])
        expected_values = [value1, value2]
        self.assertEqual(sorted(expected_values), sorted(values))
