from config import config

class BackendNotRecognizedException(Exception):
    """Possible backends are "sqlalchemy", "elasticsearch", and "djangoorm"""""
    pass

if  config['backend'] == 'sqlalchemy':
    from sqlalchemywrapper.sqlalchemywrapper import SqlAlchemyWrapper as Backend
elif config['backend'] == 'elasticsearch':
    from elasticsearchwrapper import ElasticSearchWrapper as Backend
elif config['backend'] == 'djangoorm':
    from djangoormwrapper import DjangoOrmWrapper as Backend
else:
    raise BackendNotRecognizedException
