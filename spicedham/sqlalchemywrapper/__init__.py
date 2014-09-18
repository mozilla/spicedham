import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from spicedham.backend import BaseBackend

from models import Base
from models import Store


class SqlAlchemyWrapper(BaseBackend):

    def __init__(self, config):
        """
        Create engine and session factory from config values.
        """
        self.engine = create_engine(config.get('engine',
                                    'sqlite:///./db.sqlite'))
        self.sessionFactory = sessionmaker(self.engine)
        Base.metadata.create_all(self.engine)

    def reset(self):
        session = self.sessionFactory()
        session.query(Store).delete()
        session.commit()

    def get_key(self, classifier, key, default=None):
        """
        Gets the value held by the classifier, key composite key. If it doesn't
        exist, return default.
        """
        session = self.sessionFactory()
        query = session.query(Store).filter(Store.classifier == classifier,
                                            Store.key == key)
        try:
            store = query.one()
            value = json.loads(store.value)
        except NoResultFound:
            value = default
        return value

    def set_key(self, classifier, key, value):
        """
        Set the value held by the classifier, key composite key.
        """
        session = self.sessionFactory()
        store = Store()
        value = json.dumps(value)
        store.value = value
        store.key = key
        store.classifier = classifier
        session.merge(store)
        session.commit()

    def set_key_list(self, classifier, key_value_tuples):
        """
        Given a list of tuples of classifier, key, value set them all.
        It is more efficient to use one session and merge all of the objects
        at once than to merge them individually.
        """
        session = self.sessionFactory()
        for key, value in key_value_tuples:
            store = Store()
            value = json.dumps(value)
            store.value = value
            store.key = key
            store.classifier = classifier
            session.merge(store)
        session.commit()
