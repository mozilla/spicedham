import json

config = None

def load_config():
    if config == None:
        f = open('spicedham-config.json', 'r')
        config = json.load(f)
