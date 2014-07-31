# -*- coding: utf-8 -*-
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models import WordProbability
from models import Base


class SpicedHam(object):


    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.sessionFactory = sessionmaker()
        self.sessionFactory.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def train_bulk(self, file_name):
        """Train model on input api data with an additional "spam" key"""
        f = open(self, filename, 'r')
        trainingdata = json.load(self, f)
        for result in trainingdata['result']:
            train(self, result, result['spam'])


    def train(self, result, is_spam):
        """Train the database on result. result is a dict, is_spam is a bool"""
        session = self.sessionFactory()
        query = session.query(WordProbability).filter(WordProbability.word=='*')
        try:
            total = query.one()
        except NoResultFound, e:
            total = WordProbability()
            total.word = '*'
            total.numTotal = 0
            total.numSpam = 0
        for description in result['description'].split(' '):
            description = description.lower()
            if description == '*':
                continue
            total.numTotal += 1
            query = session.query(WordProbability).filter(WordProbability.word==description)
            try:
                word = query.one()
            except NoResultFound, e:
                word = WordProbability()
                word.numTotal = 0
                word.numSpam = 0
                word.word = description
            word.numTotal += 1
            if is_spam:
                word.numSpam += 1
                total.numSpam += 1
            session.add(word)
        # Remove results with no spam from database
        query = session.query(WordProbability).filter(WordProbability.numSpam==0)
        map(session.delete, query.all())
        session.add(total)
        session.commit()


    def is_spam_from_json(self, json_response):
        """Like is_spam, but json_response is a json string"""
        return self.is_spam(json.loads(self, json_response))


    def is_spam(self, response):
        """Get the probability that a response is spam. response is a dict"""
        session = self.sessionFactory()
        query = session.query(WordProbability).filter(WordProbability.word=='*')
        # If this doesn't exist then the DB hasn't been trained
        total = query.one()
        pSpam = float(total.numSpam) / float(total.numTotal)
        # Since spam and ham are independant events
        pHam = 1.0 - pSpam
        pSpamGivenWord = pSpam
        pHamGivenWord = pHam
        for description in response['description'].split(' '):
            if description == '*':
                continue
            try:
                query = session.query(WordProbability).filter(WordProbability.word==description)
                word = query.one()
            except NoResultFound, e:
                continue
            pWord = float(word.numTotal) / float(total.numTotal)
            pWordGivenSpam = float(word.numSpam) / float(total.numSpam)
            pWordGivenHam = float(word.numTotal - word.numSpam) / float(total.numTotal - total.numSpam)

            pSpamGivenWord *= pWordGivenSpam / pWord
            pHamGivenWord *= pWordGivenHam / pWord
        return pSpamGivenWord / (pSpamGivenWord + pHamGivenWord)
