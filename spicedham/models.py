from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WordProbability(Base):
    __tablename__ = 'word_probability'
    word = Column(String, primary_key=True)
    numSpam = Column(Integer)
    numTotal = Column(Integer)

    def __unicode__(self):
        return self.word
