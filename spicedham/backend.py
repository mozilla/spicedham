from spicedham.config import load_config

from sqlalchemywrapper import SqlAlchemyWrapper
#from elasticsearchwrapper import ElasticSearchWrapper
#from djangoormwrapper import DjangoOrmWrapper


class BackendNotRecognizedException(Exception):
    """Possible backends are "sqlalchemy", "elasticsearch", and "djangoorm"""""
    pass

_backend = None

def load_backend():
    global _backend
    config = load_config()
    if _backend == None:
        if  config['backend'] == 'sqlalchemy':
            _backend = SqlAlchemyWrapper()
        elif config['backend'] == 'elasticsearch':
            _backend = ElasticSearchWrapper()
        elif config['backend'] == 'djangoorm':
            _backend = DjangoOrmWrapper()
        else:
            raise _backendNotRecognizedException
    return _backend
