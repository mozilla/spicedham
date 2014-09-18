===============
Writing Plugins
===============

Writing plugins is easy. Spiced Ham uses three different types of plugins:

* Classifiers
* Backends
* Tokenizers

Each type must inherit from its specific base class which defines the plugin's
required interface and may provide some minimal functionality. The import paths
for these plugin types are:

* ``spicedham.plugin.BasePlugin``
* ``spicedham.backend.BaseBackend``
* ``spicedham.tokenizer.BaseTokenizer``

Plugins will be loaded when a ``Spicedham`` object is instantiated.
Before instantiating a ``Spicedham`` object your plugin must be imported.
Even if the code calling ``Spicedham`` does not use the plugin it must import
it so ``Spicedham`` can find the plugin.

::

    from a_plugin import APlugin # noqa
    from spicedham import Spicedham
    # Now spicedham can use your plugin
    sh = Spicedham()

It may be useful to specify ``# noqa`` so flake8 and similar tools do not
complain.

Writing A Classifier Class
--------------------------
A classifier should inherit from ``spicedham.plugin.BasePlugin``.
A classifier should implement a ``classify`` method and optionally a ``train``
and an ``__init__`` method.
The ``classify`` method should take the following arguments:
* ``self``: Just like a normal python class method
* ``classification_type``: A type used to differentiate between separate
types of classifications, such as spam and hate speech
* ``message``: A message to be processed by the tokenizer
The ``classify`` method must return either a float between 0.0 and 1.0
represtenting the probability that the classified data was matched, or the
``classify`` function may elect not to classify this message and return
``None``.
The first three arguments of the ``train`` function are the same as the
``classify`` function. In addition, ``train`` expects a bool argument
``is_spam`` indicating whether or not the provided data is spam. ``train``
should not explicitly return anything.
The ``__init__`` method will take three arguments:
* ``self``: Just like any other python class
* ``config``: A dictionary of configuration values
* ``backend``: An instance of a ``BaseBackend`` derived class
Classifiers are expected to provide sane defaults for any config values they
require, and should document those config values as well.

Writing a Tokenizer Class
-------------------------
A tokenizer should inherit from ``spicedham.tokenizer.BaseTokenizer``.
A tokenizer should implment a ``tokenize`` function which will take a
``message`` argument. A tokenizer should return a list of strings. Below is
a simple tokenizer:

::
    import re
    from spicedham.tokenizer import BaseTokenizer

    class SimpleTokenizer(BaseTokenizer):
    
        def tokenize(message):
            # message should be a string
            return re.split(' ', message)


Writing a Backend Class
-----------------------

A backend should inherit from ``spicedham.backend.BaseBackend``.
A backend must implement the following methods:
* ``set_key``: Takes four strings, a classification type, a classifier, a key,
and dictionary value
* ``get_key``: Takes three strings, a classification type, a classifier and a
key and returns a dictionary value or None if key is not present.
May take an optional keyword argument ``default``.
* ``reset``: Drops all keys and values. Useful in tests.
A backend may additionally implement the following methods:
* ``set_key_list``: Takes a string classifier and a list of key, value tuples.
This may be useful for bulk commits from a database. A default implementation
which uses ``set_key`` is provided.
* ``get_key_list``: Similar to ``set_key_list``, takes a string classifier and
a list of keys. Returns a list of dictionaries or Nones. May take an optional
keyword argument ``default``.  A default implementation which uses ``get_key``
is provided.
* ``__init__``: A backend's constructor must take a config dictionary.
Backends are responsible for specifying and DB models they may require.

A Sample Classifier Tutorial
----------------------------
Input gets a lot of spam where the spammer rails on Mozilla for being "A bunch
of Nazis". This is obviously spam, and it's safe to conclude that any message
mentioning the word "Nazi" is spam. In this tutorial we'll write a spicedham
pluging to give a high probability to any message which uses a specified word
in the config file.
Since this plugin is so simple no training phase will be required.

First, let's import the base class for the plugin. You should go take a look at
this base class to see what functions it implements.

::
	from spicedham.baseplugin import BasePlugin

Next, we'll need to declare the plugin class and the ``__init__`` function.

::
	class WordFilter(BasePlugin):
		
		def __init___(self, config, backend):
			pass

We'll get the actualy word we want from the config dictionary
We should make the key be the name of our plugin in lower case (like the
package name) and the value be a dictionary. This is so we have proper
namespacing of configuration values. Here is an example configuration for this
plugin:

::
    config = {
        # ... other config values ...
        'wordfilter' = {
            'word': 'nazi'
            },
    }

Now let's load the configuration dictionary in our ``__init__`` function.

::

	def __init__(self, config, backend):
        # Make sure to provide sane defaults
        wordfilter_config = config.get('wordfilter', {})
		self.word = wordfilter_config.get('word', '')

Next we'll write the actual ``classify`` function. The ``classify`` function
returns either a float representing the probability that the message is spam
between 0.0 and 1.0 or, if the plugin is unable to determine reasonably a
probability, just None

::
	...
	def classify(self, classification_type response):
		if self.word in response:
			return 1.0
		else:
			return None

That's it! We just wrote a sample plugin. For more examples of interesting
things which plugins can do, take a look at the plugins ``spicedham/bayes.py``
or ``spicedham/nonsensefilter.py``.
For extra credit and gold stars you can modify this function to take a list of
blasklisted words from the config, add docstrings, and explore the
spicedham backend infrastructure.

A Sample Backend Tutorial
-------------------------
Redis is an easy to use key value store. We'll implement a minimal backend
using redis.

First install redis using pip:

::
    $ pip install redis

Next define our class:

::
    import json
    import redis
    from spicedham.backend import BaseBackend

    class RedisWrapper(BaseBackend):
        ...

We'll need some way to connect to redis so we'll create our server in
``__init__`` and grab what we need from the config:

::
    def __init__(self, config):
        rediswrapper_config = config.get('rediswrapper', {})
        host = rediswrapper_config.get('host', 'localhost')
        port = rediswrapper_config.get('port', 6379)
        db = rediswrapper_config.get('db', 0)
        self.redis_server = redis.StrictRedis(host=host, port=port, db=db)

We need to be able to conver between dictionaries and strings, so we'll use 
``json.loads`` and ``json.dumps``.
Now we need to be able to set keys:

::
    def set_key(self, classification_type, classifier, key, value):
        value = json.dumps(value)
        redis_server.set(classification_type + classifier + key, value)

We should make our ``get_keys`` function act like ``dict.get`` and give it an
optional default value of None.

::
    def get_key(self, classification_type, classifier, key, default=None):
        value = redis_server.get(classification_type + classifier + key)
        if value is None:
            return default
        return json.loads(value)

Finally, we need to implement a ``reset`` function to remove all keys and
values. This is really helpful for testing.

::
    def reset(self):
        redis_server.flushdb()

You're done! Writing backends can be quite painless! For fun you can add
docstrings and explore the ``sqlalchemywrapper`` backend.
