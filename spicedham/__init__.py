from pkg_resources import iter_entry_points


class NoBackendFoundError(Exception):
    pass


class Spicedham(object):

    _classifier_plugins = []
    backend = None
    # Default config values
    config = {
        'backend': 'sqlalchemy',
        'engine': 'sqlite:///./spicedham.db',
    }

    def __init__(self):
        """
        Load config, backend, and plugins
        """
        self._load_config()
        self._load_backend()
        self._load_plugins()

    def _load_plugins(self):
        # In order to use the plugins config and backend must be loaded.
        self._classifier_plugins = []
        for plugin in iter_entry_points(group='spicedham.classifiers', name=None):
            pluginClass = plugin.load()
            self._classifier_plugins.append(pluginClass(self))

    def _load_backend(self):
        try:
            entry_point = iter_entry_points(group='spicedham.backends',
                name=self.config['backend'])
            entry_point = next(entry_point)
        except StopIteration:
            raise NoBackendFoundError()
        pluginClass = entry_point.load()
        self.backend = pluginClass()

    def _load_config(self):
        for config_plugin in iter_entry_points(group='spicedham.config', name=None):
            config_plugin_obj = config_plugin.load()
            for key in config_plugin_obj.keys():
                config[key] = config_plugin_obj[key]

    def train(self, training_data, match):
        """
        Calls each plugin's train function.
        `training_data` is an iterable of strings. `match` is a boolean
        indicating whether the training data should be matched.
        For instance, if you're filtering spam `match` will be True for spam,
        and False for a normal message.
        """
        for plugin in self._classifier_plugins:
            plugin.train(training_data, match)

    def classify(self, classification_data):
        """
        Calls each plugin's classify function and averages the results.
        `classification_data` is an iterable of strings.
        """
        average_score = 0
        total = 0
        for plugin in self._classifier_plugins:
            value = plugin.classify(classification_data)
            # Skip _plugins which give a score of None
            if value != None:
                total += 1
                average_score += value
        # On rare occasions no _plugins will give scores. If so, return 0
        if total > 0:
            return float(average_score) / float(total)
        else:
            return 0
