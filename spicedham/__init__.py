from pkg_resources import iter_entry_points

from config import config


plugins = []
for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
    pluginClass = plugin.load()
    plugins.append(pluginClass())


def train(training_data, is_spam):
    for plugin in plugins:
        plugin.train(training_data, is_spam)


def classify(classification_data):
    average_score = 0
    for plugin in plugins:
        average_score += plugin.classify(classification_data)
    return average_score / len(plugins)
        plugin.setup()
