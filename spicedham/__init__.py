from pkg_resources import iter_entry_points

from config import config


plugins = []
for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
    plugins.append(plugin.load())


def train(training_data, is_spam):
    for plugin in plugins:
        plugin.train(training_data, is_spam)


def classify(classification_data, is_spam):
    average_score = 0
    for plugin_method in plugins:
        average_score += plugin_method(classification_data, is_spam)
    return average_score / len(plugins)


def setup():
    for pluginMethod in plugins:
        print pluginMethod
        print type(pluginMethod)
        pluginMethod()
