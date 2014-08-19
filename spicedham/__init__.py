from pkg_resources import iter_entry_points

from config import config


plugins = []
for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
    pluginClass = plugin.load()
    plugins.append(pluginClass())


def train(tag, training_data, is_spam):
    for plugin in plugins:
        plugin.train(tag, training_data, is_spam)


def classify(tag, classification_data):
    average_score = 0
    total = 0
    for plugin in plugins:
        value = plugin.classify(tag, classification_data)
        if value != None:
            total += 1
            average_score += value
    if total > 0:
        return average_score / total
    else:
        return 0
