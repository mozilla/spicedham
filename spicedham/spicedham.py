#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sqlalchemy

from database import DB

# For performance testing
import logging
import time

class SpicedHam(object):
    """"A spam filtering library developed for input.mozilla.org"""

    def __init__(self):
        logging.basicConfig(filename='blacklist.log',level=logging.DEBUG)
        self._load_config('./config.json')
        self.db = DB()
        self.db.init_db(self.)

    def _load_config(self, file_name):
        if not file_name[-5:] == '.json':
            raise "File format not recognized"
        f = open(file_name, 'r')
        json_file_contents = f.read()
        self.config = json.loads(json_file_contents)

    def _init_db(self):
        sqlalchemy.create_engine(self.config['db']['engine'])
        session = sqlalchemy.create_session()

    def blacklist_filter(self, response):
        """Check response dictionary against blacklist and updates spamscore"""
        if self.config.get('blacklist') == None:
            return
        debug_start_time = time.time()
        logging.debug("Beginning blacklist filter. Time: " + str(debug_start_time))
        for key in self.config['blacklist'].keys():
            if key in response:
                for attr in self.config['blacklist'][key]:
                    for elem in response[key]:
                        if attr in elem:
                            response['spamscore'] += 0.2
        debug_end_time = time.time()
        logging.debug("Blacklist filter finished. Time: " + str(debug_end_time) + "\nTime delta: " + str(debug_end_time - debug_start_time))

    def is_spam(self, response):
        """Takes a json object and returns a 0.0-1.0 probility that it's spam"""
        if type(response) == str:
            response = json.loads(response)
        # We presume innocence
        response['spamscore'] = 0
        self.blacklist_filter(response)
        #print 'spamscore', response['spamscore']
        return response['spamscore']
