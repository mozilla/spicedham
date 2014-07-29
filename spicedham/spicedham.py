#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import UniqueConstraint

from models import Probability

# For performance testing
import logging
import time

class SpicedHam(object):
    """"A spam filtering library developed for input.mozilla.org"""

    def __init__(self):
        """Load configuration and connect to the database"""
        logging.basicConfig(filename='blacklist.log',level=logging.DEBUG)
        self._load_config('./config.json')
        self.engine = create_engine(self.config['db']['engine_name'])
        self.sessionFactory = sessionmaker()
        self.sessionFactory.configure(bind=self.engine)

    def train_db_from_data(self, file_name):
        """Iterate through the given json"""
        f = open(filename, 'r')
        resp = json.load(f)
        totals = Probability(description='totals', field='totals')
        totals.total_occurences = resp['count']
        totals.total_spam = 0
        session = self.sessionFactory()
        for response in resp['results']:
            for bigram in response['description_bigrams']:       
                pair = self._get_db_pair(bigram, 'description_bigrams')
                pair.total_occurences += 1
                if response['is_spam']:
                    pair.spam_occurences += 1
                    totals.spam_occurences += 1
                session.add(pair)
        session.add(totals)
        session.commit()

    def _load_config(self, file_name):
        if not file_name[-5:] == '.json':
            raise "File format not recognized"
        f = open(file_name, 'r')
        self.config = json.load(f)

    def _get_db_pair(self, field, description):
        query = (session
               .query(Probability)
               .filter(Probability.description==description)
               .filter(Probability.field==field))
        try:
            pair = query.one()
        except MultipleResultsFound, e:
            pair = Probability(description=description, field=bigram)
        return pair

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
                            response['spamscore'] *= 1.2
        debug_end_time = time.time()
        logging.debug("Blacklist filter finished. Time: " + str(debug_end_time) + "\nTime delta: " + str(debug_end_time - debug_start_time))

    def is_spam(self, response):
        """Takes a json object and returns a 0.0-1.0 probility that it's spam"""
        if type(response) == str:
            response = json.loads(response)
        # spamscores are multiplied
        response['spamscore'] = 1
        #self.blacklist_filter(response)
        return response['spamscore']

    def naive_bayes(self, response):
        """Determine whether the given response is spam and update the model"""
        session = self.sessionFactory()
        totals = self._get_db_pair('totals', 'totals')
        for bigram in response['description_bigrams']:
            bigramData = self._get_db_pair('description_bigrams', bigram)
            pBigram = bigramData.total_occurences
            pBigramGivenSpam = bigramData.total_spam / pBigram
            pSpam = totals.total_spam / totals.total_occurences
            response['spamscore'] *= pBigramGivenSpam * pSpam / pBigram
