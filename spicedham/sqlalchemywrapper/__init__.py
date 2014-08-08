import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from spicedham.basewrapper import BaseWrapper
from spicedham import config

from models import Base
from models import Store

class EngineNotRecognizedError(Exception):
    pass

class EngineNotFoundError(Exception):
    """There was no engine specified in the config"""
    pass

class SqlAlchemyWrapper(BaseWrapper):

    def __init__(self):
        try:
            self.engine = create_engine(config['engine'])
            self.sessionFactory = sessionmaker(self.engine)
            Base.metadata.create_all(self.engine)
        except KeyError, e:
            raise EngineNotFoundError

    def get_key(self, key, default=None):
        session = self.sessionFactory()
        query = session.query(Store).filter(Store.key==key)
        try:
            store = query.one()
            value = json.loads(store.value)
        except NoResultFound, e:
            value = default
        return value

    def set_key(self, key, value):
        session = self.sessionFactory()
        store = Store()
        value = json.dumps(value)
        store.value = value
        store.key = key
        session.merge(store)
        session.commit()
