import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from spicedham.basewrapper import BaseWrapper
from spicedham.config import load_config

from models import Base
from models import Store

# TODO: not necessary
class EngineNotRecognizedError(Exception):
    pass

class EngineNotFoundError(Exception):
    """There was no engine specified in the config"""
    pass

class SqlAlchemyWrapper(BaseWrapper):

    def __init__(self):
        """
        Create engine and session factory from config values.
        """
        config = load_config()
        try:
            self.engine = create_engine(config['engine'])
            self.sessionFactory = sessionmaker(self.engine)
            Base.metadata.create_all(self.engine)
        except KeyError, e:
            raise EngineNotFoundError

    def reset(self, really):
        if really:
            session = self.sessionFactory()
            everything = session.query(Store).delete()
            session.commit()
        else:
            pass


    def get_key(self, classifier, key, default=None):
        """
        Gets the value held by the classifier, key composite key. If it doesn't exist,
        return default.
        """
        session = self.sessionFactory()
        query = session.query(Store).filter(Store.classifier==classifier, Store.key==key)
        try:
            store = query.one()
            value = json.loads(store.value)
        except NoResultFound, e:
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
