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
            train(self, result)


    def train(self, result, is_spam):
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
        session.add(total)
        session.commit()


    def is_spam_from_json(self, json_response):
        return self.is_spam(json.loads(self, json_response))


    def is_spam(self, response):
        # If this doesn't exist then the DB hasn't been trained
        session = self.sessionFactory()
        query = session.query(WordProbability).filter(WordProbability.word=='*')
        total = query.one()
        import q

        pSpamGivenBigram = float(total.numSpam) / float(total.numTotal)
        q(total.numSpam)
        q(total.numTotal)
        q(pSpamGivenBigram)
        pHamGivenBigram = 1.0 - pSpamGivenBigram
        q(pHamGivenBigram)
        for description in response['description'].split(' '):
            try:
                query = session.query(WordProbability).filter(WordProbability.word==description)
                word = query.one()
            except NoResultFound, e:
                continue
            if word.numSpam == 0:
                continue
            q(total.numTotal)
            q(word.numTotal)
            q(word.numSpam)
            pBigram = float(word.numTotal) / float(total.numTotal)
            q(pBigram)
            pBigramGivenSpam = float(word.numSpam) / float(word.numTotal)
            q(pBigramGivenSpam)
            pBigramGivenHam = float(word.numTotal - word.numSpam) / float(word.numTotal)
            q(pBigramGivenHam)
            pSpamGivenBigram *= float(pBigramGivenSpam) / float(pBigram)
            pHamGivenBigram *= float(pBigramGivenHam) / float(pBigram)
            q(pSpamGivenBigram)
            q(pHamGivenBigram)
        pSpam = float(pSpamGivenBigram) / float(pHamGivenBigram)
        return pSpam
