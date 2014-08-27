============
Installation
============

At the command line::

    $ pip install spicedham

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv spicedham
    $ pip install spicedham

=============
Configuration
=============

To use spicedham you need a configuration file to specify your backend data
store as well as the plugins you intend to load. This configuration file is
written in json and called `spicedham-config.json`. It should be in the
directory from which the application will be run. There are two options for
backend datastores, SQLAlchemy and the Django ORM.
A sample configuration is included in the project root as
``spicedham-config.json.dist``

Configuration for SQLAlchemy
----------------------------
To use the SQLAlchemy backend you will need to set the `"backend"` key to
`"sqlalchemy"`. You will also need to specify a database engine. Below is a
sample configuration:

::
	{
		"backend": "sqlalchemy",
		"engine": "sqlite:///:memory:"
	}
The engine parameter will be passed to SQLAlchemy when constructing the engine.
Consuult the SQLAlchemy documentation for valid engines. Note that this backend
probably will not work with Flask-SQLAlchemy.

Configuration for the Django ORM
--------------------------------
To use the Django ORM you will need to set the `"backend"` key to
`"django-orm"`. You will need to configure the Django ORM according separately
according to the django documentation. Below is a sample configuration:

::
	{
		"backend": "django-orm"
	}

Configuring Plugins
-------------------
Plugins will specify how they will be configured in their own documentation.
Plugin configuration variables will be read from a section in the configuration
file named after the plugin. Below is an example of how to configure the
*NonsenseFilter* plugin:

::
	{
		...other configuration options here...
		"nonsensefilter": {
			"filter_match": 1,
			"filter_miss": null
		}
	}
