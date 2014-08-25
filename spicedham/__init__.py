from pkg_resources import iter_entry_points

from spicedham.config import load_config
from spicedham.backend import load_backend

_plugins = None

def load_plugins():
    """
    If not already loaded, load plugins.
    """
    global _plugins
    if _plugins == None:
        # In order to use the plugins config and backend must be loaded.
        load_backend()
        load_config()
        _plugins = []
        for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
            pluginClass = plugin.load()
            _plugins.append(pluginClass())


def train(tag, training_data, is_spam):
    """
    Calls each plugin's train function.
    """
    for plugin in _plugins:
        plugin.train(tag, training_data, is_spam)


def classify(tag, classification_data):
    """
    Calls each plugin's classify function and averages the results.
    """
    average_score = 0
    total = 0
    for plugin in _plugins:
        value = plugin.classify(tag, classification_data)
        # Skip _plugins which give a score of None
        if value != None:
            total += 1
            average_score += value
    # On rare occasions no _plugins will give scores. If so, return 0
    if total > 0:
        return average_score / total
    else:
        return 0
