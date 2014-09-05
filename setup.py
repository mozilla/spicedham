#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def get_version():
    VERSIONFILE = os.path.join('spicedham', '__init__.py')
    VSRE = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(VERSIONFILE, 'rt').read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name='spicedham',
    version='0.0.0',
    description='Spam filter library developed for input',
    long_description=readme + '\n\n' + history,
    author='Ian Kronquist',
    author_email='iankronquist@gmail.com',
    url='https://github.com/mozilla/spicedham',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points = {
        'spicedham.classifiers': [
            'bayes = spicedham.bayes:Bayes', 
            'digit_destroyer = spicedham.digitdestroyer:DigitDestroyer',
            'nonsense_filter = spicedham.nonsensefilter:NonsenseFilter',
            ],
        'spicedham.backends': [
            'sqlalchemy = spicedham.sqlalchemywrapper:SqlAlchemyWrapper'
        ]
    },
    license="MPL v2",
    zip_safe=True,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MPL v2',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
