from spicedham.config import config

from sqlalchemywrapper import SqlAlchemyWrapper
#from elasticsearchwrapper import ElasticSearchWrapper
#from djangoormwrapper import DjangoOrmWrapper


class BackendNotRecognizedException(Exception):
    """Possible backends are "sqlalchemy", "elasticsearch", and "djangoorm"""""
    pass

if  config['backend'] == 'sqlalchemy':
    Backend = SqlAlchemyWrapper()
elif config['backend'] == 'elasticsearch':
    Backend = ElasticSearchWrapper()
elif config['backend'] == 'djangoorm':
    Backend = DjangoOrmWrapper()
else:
    raise BackendNotRecognizedException
