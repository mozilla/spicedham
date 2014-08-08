from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Store(Base):
    __tablename__ = 'store'
    key = Column(String, primary_key=True)
    value = Column(String)

    def __unicode__(self):
        return unicode(key)
