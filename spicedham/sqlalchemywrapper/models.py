from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()

class Store(Base):
    __tablename__ = 'store'
    key = Column(String)
    tag = Column(String)
    value = Column(String)
    __table_args__ = (PrimaryKeyConstraint('key', 'tag'),)

    def __unicode__(self):
        return unicode(key)
