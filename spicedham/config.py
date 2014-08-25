import json

_config = None

def load_config():
    global _config
    if _config == None:
        f = open('spicedham-config.json', 'r')
        _config = json.load(f)
    return _config
