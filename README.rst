=========
spicedham
=========

Spam filter library developed for input
--------

:Code:         https://github.com/mozilla/spicedham/
:Issues:       https://github.com/mozilla/spicedham/issues
:License:      Mozilla Public License Version 2.0; See LICENSE
:Contributors: See AUTHORS.rst


Install
=======

From PyPI (doesn't work, yet)
-----------------------------

Run::

    $ pip install spicedham

Configuration
-------------
See ``docs/intsallation.rst``.


For hacking
-----------

Run::

    # Get the code
    $ git clone https://github.com/mozilla/spicedham

    # Create a virtualenvironment
    $ pip install -e .

API
---
The API for spicedham is simple. There are three steps you need to do to
classify spam:
1. Load the plugins:

:: 
	from spicedham import load_plugins
	load_plugins()

2. Train on data. The arguments are:
	- Some tag so different kinds of data don't get mixed up
	- A list of words or other strings which can be scanned for spamminess
	- A boolean indicating whether a message is spam

::
	from spicedham import train
	train('user_message', ['I', 'love', 'firefox'], False)
	train('user_message', ['SPAM!'], True)

3. Classify some data. The first two arguments are the same as above:

::
	from spicedham import classify
	classify('user_message', ['maybe', 'I'm', 'spam', 'or', 'maybe', 'not'])
