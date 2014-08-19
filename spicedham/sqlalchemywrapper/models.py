from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()

class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    tag = Column(String)
    value = Column(String)
    __table_args__ = (UniqueConstraint('key', 'tag'),)

    def __unicode__(self):
        return unicode(key)
