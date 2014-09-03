from pkg_resources import iter_entry_points

_config = None

def load_config():
    global _config
    if _config == None:
        # Default config values
        _config = {
            'backend': 'sqlalchemy',
            'engine': 'sqlite:///:memory:',
            'nonsensefilter': {'filter_match': 1, 'filter_miss': None},
            'digitdestroyer': {'filter_match': 1, 'filter_miss': None},
        }
        for config_plugin in iter_entry_points(group='spicedham.config', name=None):
            config_plugin_obj = config_plugin.load()
            for key in config_plugin_obj.keys():
                _config[key] = config_plugin_obj[key]
    return _config
