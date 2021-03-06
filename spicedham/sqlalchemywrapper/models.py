from sqlalchemy import Column, String
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
    classifier = Column(String)
    classification_type = Column(String)
    value = Column(String)
    __table_args__ = (PrimaryKeyConstraint('key', 'classification_type',
        'classifier'),)

    # TODO: Add the tag here
    def __unicode__(self):
        return unicode(self.key)
