===============
Writing Plugins
===============

Writing plugins is easy. Plugins use setuptools' native plugin system so they
can be distributed separately from spicedham and automatically detected. All
plugins should inherit from the ``spicedham.baseplugin.BasePlugin`` class.
There are three important files that will need to be made or modified when
writing a plugin. The first is the plugin itself.

Writing the Class
------------------
Plugins will be loaded when ``spicedham.load_plugins`` is called.
A plugin should implement a ``classify`` method and optionally a ``train``
method.
The ``classify`` method should take the following arguments:
* ``self``: just like a normal python class method
The ``classify`` method must return either a float between 0.0 and 1.0
represtenting the probability that the classified data is spam, or the
``classify`` function may elect not to classify this message and return
``None``.
The first two arguments of the ``train`` function are the same as the
``classify`` function. In addition, ``train`` expects a bool argument
``is_spam`` indicating whether or not the provided data is spam. ``train``
should not explicitly return anything.
If a plugin requires setup, for instance if it needs to load the spicedham
backend or load the spicedham config, it should use ``__init__`` just like any
other python class.

Getting Spicedham Configuration Values
--------------------------------------
To access spicedham configuration import the ``spicedham.config.load_config``
function. It will return a dictionary of configuration options in the same form
as the ``spicedham-config.json`` file. (Hint: we literally call json.load on
the contents of the file). For more information about this config file, see the
**Configuration** section of the installation documentation.

Accessing the Spicedham Backend
-------------------------------

To access the spicedham backend, import the ``spicedham.backend.load_backend``
function. When called, it will return a subclass of the 
``spicedham.basewrapper.BaseWrapper`` class.

Declaring the Plugin with ``setup.py``
--------------------------------------
To advertise a plugin so spicedham will load it, write and install the plugin's
``setup.py`` file. Documentation on ``setup.py`` can be found here_.
The specific section needed to actually declare the plugin is called
``entry_points``. Your plugin will need to declare a ``spicedham.classifier``
entry point, which may be a single string or a list of strings representing
the python import path to your plugin, followed by a single colon, followed by the class name.
Below is an example ``setup.py``:

::
	setup(
		name='plugin',
		entry_points = 'import.path.to.plugin.file:PluginClass',
	)

.. _here: https://docs.python.org/2/distutils/setupscript.html

A Sample Plugin Tutorial
------------------------
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
		
		def __init___(self):
			pass

We'll get the actualy word we want from the config file. To do this we'll need
to edit the config file:

::
	{
		...other config options...
		"wordfilter": {
			"word": "nazi"
		}
	}

We should make the key be the name of our plugin in lower case (like the
package name) and the value be a dictionary. This is so we have proper
namespacing of configuration values.

Now let's go back to the top and import the function we'll need to load the
config.

::
	from spicedham.config import load_config

Now let's load the configuration dictionary in our ``__init__`` function.

::
	...
	def __init__(self):
		config = load_config()
		self.word = config['wordfilter']['word']

Next we'll write the actual ``classify`` function. The ``classify`` function
returns either a float representing the probability that the message is spam
between 0.0 and 1.0 or, if the plugin is unable to determine reasonably a
probability, just None

::
	...
	def classify(self, response):
		if self.word in response:
			return 1.0
		else:
			return None

That's it! We just wrote a sample plugin. For more examples of interesting
things which plugins can do, take a look at the plugins ``spicedham/bayes.py``
or ``spicedham/nonsensefilter.py``.
For extra credit and gold stars you can modify this function to take a list of
blasklisted words from the config file, add docstrings, and explore the
spicedham backend infrastructure.
