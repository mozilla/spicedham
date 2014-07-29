from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Model = declarative_base()

class Probability(Model):
    __tablename__ = 'probability'
    field = Column(String)
    description = Column(String)
    total_occurences = Column(Integer)
    spam_occurences = Column(Integer)
    __table_args__ = (UniqueConstraint('field', 'description'),)

# class UserAgents(Model):
#     __tablename__ = 'useragents'
#     # TODO: find all the fields in a user agent to do clustering
#     field = Column(Integer)
