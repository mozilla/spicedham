from pkg_resources import iter_entry_points

from spicedham.config import load_config

#TODO: wrap all of these in a threadsafe class
_classifier_plugins = None
_backend = None

def load_plugins():
    """
    If not already loaded, load plugins.
    """
    global _classifier_plugins
    if _classifier_plugins == None:
        # In order to use the plugins config and backend must be loaded.
        _classifier_plugins = []
        load_backend()
        for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
            pluginClass = plugin.load()
            _classifier_plugins.append(pluginClass())

def load_backend():
    global _backend
    if _backend == None:
        # If django is installed and the djangoorm plugin is registered, choose that
        try:
            import django
            #TODO: This is ugly
            djangoorm = iter_entry_points(group='spicedham.backends', name='djangoorm')
            if djangoorm:
                entry_point = next(djangoorm)
                djangoOrmClass = entry_point.load()
                _backend = djangoOrmClass()
        # Else choose the first one
        except ImportError:
            #TODO: handle the case where no plugins are installed
            #TODO: maybe we should pull the name from the config instead
            plugin = next(iter_entry_points(group='spicedham.backends', name=None))
            pluginClass =  plugin.load()
    return _backend

def train(training_data, is_spam):
    """
    Calls each plugin's train function.
    """
    for plugin in _classifier_plugins:
        plugin.train(training_data, is_spam)


def classify(classification_data):
    """
    Calls each plugin's classify function and averages the results.
    """
    average_score = 0
    total = 0
    for plugin in _classifier_plugins:
        value = plugin.classify(classification_data)
        # Skip _plugins which give a score of None
        if value != None:
            total += 1
            average_score += value
    # On rare occasions no _plugins will give scores. If so, return 0
    if total > 0:
        return average_score / total
    else:
        return 0
