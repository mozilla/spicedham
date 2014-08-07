import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from spicedham.basewrapper import BaseWrapper
from spicedham import config

from models import Base
from models import Store

class SqlAlchemyWrapper(BaseWrapper):

    def setup(self):
        self.engine = config['engine']
        self.sessionFactory = sessionmaker()
        Base.metadata.create_all(self.engine)

    def get_key(key, default=None):
        session = self.sessionFactory()
        query = session.query(Store).filter(Store.key==key)
        try:
            store = query.one()
            value = json.loads(store.value)
        except NoResultFound, e:
            value = default
        return value

    def set_key(key, value):
        session = self.sessionFactory()
        store = Store()
        value = json.dump(value)
        store.value = value
        store.key = key
        session.add(store)
        session.commit()
