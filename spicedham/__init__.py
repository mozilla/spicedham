# -*- coding: utf-8 -*-
import json

from spicedham.models import WordProbability


def train_bulk(file_name):
    """Train model on input api data with an additional "spam" key"""
    f = open(filename, 'r')
    trainingdata = json.load(f)
    for result in trainingdata['result']:
        train(result)


def train(result, is_spam):
    try:
        total = WordProbability.objects.get(word='*')
    except DoesNotExist, e:
        total = WordProbability(word='*', numTotal=0, numSpam=0)
    for description in result['description'].split(' '):       
        if description == '*':
            continue
        total.numTotal += 1
        try:
            word = WordProbability.objects.get(word=description)
        except DoesNotExist, e:
            word = WordProbability(numTotal=0, numSpam=0, word=description)
        word.numTotal += 1
        if is_spam:
            word.numSpam += 1
            total.numSpam += 1
        word.save()
    total.save()


def is_spam_from_json(json_response):
    return is_spam(json.loads(json_response))


def is_spam(response):
    pSpamGivenBigram = pSpam
    pHamGivenBigram = pHam
    # If this doesn't exist then the DB hasn't been trained
    total = WordProbability.objects.get(word='*')
    for bigram in response['description_bigrams']:
        try:
            word = WordProbability.objects.get(word=bigram)
        except DoesNotExist, e:
            continue
        pBigram = word.numTotal / total.numTotal
        pBigramGivenSpam = word.numSpam / word.numTotal
        pBigramGivenHam = (word.numTotal - word.numSpam) / word.numTotal
        pSpamGivenBigram *= pBigramGivenSpam / pBigram
        pHamGivenBigram *= pBigramGivenHpam / pBigram
    pSpam = pSpamGivenBigram / pHamGivenBigram
    return pSpam
