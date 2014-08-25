from pkg_resources import iter_entry_points

from spicedham.config import config

# TODO: Wrap all of this in an object with this in an __init__ function
plugins = []
for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
    pluginClass = plugin.load()
    plugins.append(pluginClass())


def train(tag, training_data, is_spam):
    """
    Calls each plugin's train function.
    """
    for plugin in plugins:
        plugin.train(tag, training_data, is_spam)


def classify(tag, classification_data):
    """
    Calls each plugin's classify function and averages the results.
    """
    average_score = 0
    total = 0
    for plugin in plugins:
        value = plugin.classify(tag, classification_data)
        # Skip plugins which give a score of None
        if value != None:
            total += 1
            average_score += value
    # On rare occasions no plugins will give scores. If so, return 0
    if total > 0:
        return average_score / total
    else:
        return 0
