=========
spicedham
=========

Spam filter library developed for input
=======================================

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

For hacking
-----------

Run::

    # Get the code
    $ git clone https://github.com/mozilla/spicedham

    # Create a virtualenvironment
    $ virtualenv ../venv
    $ source ../venv/bin/activate
    # Install dependencies
    $ pip install -r requirements.txt
    # Install the code
    $ pip install -e .

Running tests
=============

Run:

::
    
    $ nosetests

Configuration
=============

See ``docs/intsallation.rst``.


API
===

The API for spicedham is simple. There are three steps you need to do to
classify spam:

1. Instantiate a SpicedHam object:

    ::

        from spicedham import SpicedHam
        spicedham = SpicedHam()

    Optionally you can pass dictionary of configuration values like so:

    ::

        config = {
            'backend': 'SqlAlchemyWrapper', # The class name of your backend
            'engine': 'sqlite:///:memory:', # Needed by SqlAlchemyWrapper
            'tokenizer': 'SplitTokenizer',  # The class name of your tokenizer
        }
        spicedham = SpicecHam(config)

2. Train on data. The arguments are:

   * A string type which indicates the type of classification (to differentiate
     between, say, spam and hate speech)
   * A string message which can be split up by your chosen tokenizer.
   * A boolean indicating whether classifiers should match the message

   ::

       spicedham.train('spam', 'I love Firefox!', False)
       spicedham.train('spam', 'SPAMMY NONSENSE AND HATE SPEECH!', True)

3. Classify some data. ``chance_matched`` is a probability that the message was
   what you're searching for and will be between 0 and 1 (inclusive).

   ::

       chance_matched = spicedham.classify('spam', 'maybe I'm spam or maybe not')
