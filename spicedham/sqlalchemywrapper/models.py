from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

# TODO: Will doesn't want things to run on module import, but I believe this
# is what the sqlalchemy docs say to do
Base = declarative_base()

class Store(Base):
    """
    A model representing a key value store.
    tag and key are composite primary keys (and thus unique as a pair).
    All columns are strings. Value is typically serialized json.
    """
    __tablename__ = 'store'
    key = Column(String)
    tag = Column(String)
    value = Column(String)
    __table_args__ = (PrimaryKeyConstraint('key', 'tag'),)

    #TODO: Add the tag here
    def __unicode__(self):
        return unicode(key)
