=============
Configuration
=============

When instantiating a SpicedHam object you may optionally pass a dictionary of
configuration variables. If you choose to pass this, you must specify at least
a key named ``backend`` and a key named ``tokenizer``. The value for the
``backend`` key must be the name of a subclass of ``BaseBackend``. The value
for the ``tokenizer`` key must be the name of a sublass of ``BaseTokenizer``.
An example configuration, which is the default, follows:

::
    config = {
        'backend': 'SqlAlchemyWrapper',
        'engine': 'sqlite:///./spicedham.db', # Required by SqlAlchemyWrapper
        'tokenizer': 'SplitTokenizer',
    }


Configuration for SQLAlchemy
----------------------------
To use the SQLAlchemy backend you will need to set the `"backend"` key to
`"SqlAlchemyWrapper"`. You will also need to specify a database engine. Below
is a sample configuration:

::
	{
		"backend": "SqlAlchemyWrapper",
		"engine": "sqlite:///:memory:"
	}

The ``engine`` parameter will be passed to SQLAlchemy when constructing the
engine. Consult the SQLAlchemy documentation for valid engines. Note that this
backend probably will not work with Flask-SQLAlchemy.

Configuring Plugins
-------------------
Plugins will specify how they will be configured in their own documentation.
Plugin configuration variables will be read from a section in the configuration
dict named after the plugin. Below is an example of how to configure the
*NonsenseFilter* plugin:

::
	{
		...other configuration options here...
		"nonsensefilter": {
			"filter_match": 1,
			"filter_miss": null
		}
	}
