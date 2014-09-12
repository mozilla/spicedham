import os
import re
import tarfile
import json
import requests
import time
from datetime import datetime

from spicedham import Spicedham
THRESHHOLD = 0.5

def test_on_training_data():
    print 'testing against the training data set'
    test_file(os.path.join('corpus', 'train'))


def test_on_spam_data():
    print 'testing against the spam data set'
    test_file(os.path.join('corpus', 'spam'))

def train_on_api_like_data(file_name):
    time_start = time.time()
    train_time = 0
    if os.path.exists(file_name):
        print 'training on the file ' + file_name
        description_spam = []
        description_ham = []
        with open(file_name, 'r') as f:
            j = json.load(f)
        for result in j['results']:
            if result['control']:
                continue
            train_start = time.time()
            sh.train(result['description'], result['spam'])
            train_time += time.time() - train_start 
    else:
        print 'crowd corpus not found. continuing without it.'
    print 'total time', time.time() - time_start 

def test_file(data_file_name):
    print 'testing on ' + data_file_name
    test_results = {
        'Total': [],
        'True+': [],
        'False+': [],
        'True-': [],
        'False-': [],
        'Error': [],
    }
    with open(data_file_name, 'r') as f:
        j = json.load(f)
        for resp in j['results']:
            test_results['Total'].append(resp['id'])
            probability = sh.classify(resp['description'])
            if 0.0 > probability > 1.0:
                test_results['Errors'].append(resp['id'])
            if probability > THRESHHOLD:
                if resp['spam']:
                    test_results['True+'].append(resp['id'])
                else:
                    test_results['False+'].append(resp['id'])
            else:
                if resp['spam']:
                    test_results['False-'].append(resp['id'])
                else:
                    test_results['True-'].append(resp['id'])
        show_results(test_results)

def show_results(test_results):
    red = '\033[0;31m'
    green = '\033[0;32m'
    nocolor = '\033[0m'
    print 'False negatives: ', test_results['False-']
    print '{0} responses analyzed'.format(len(test_results['Total']))
    print 'True positives:  {0} ({1}%)'.format(len(test_results['True+']),
        percent(len(test_results['True+']), len(test_results['Total'])))
    print 'False negatives: {0} ({1}%)'.format(len(test_results['False-']),
        percent(len(test_results['False-']), len(test_results['Total'])))
    print 'True negatives:  {0} ({1}%)'.format(len(test_results['True-']),
        percent(len(test_results['True-']), len(test_results['Total'])))
    print 'False positives: {0} ({1}%)'.format(len(test_results['False+']),
        percent(len(test_results['False+']), len(test_results['Total'])))
    print 'Errors:          {0} ({1}%)'.format(len(test_results['Error']),
        percent(len(test_results['Error']), len(test_results['Total'])))

def percent(numerator, denominator):
    if denominator == 0: return 0
    return round(float(numerator) / float(denominator) * 100, 3)

def test_on_api_data(url='https://input.mozilla.org/api/v1/feedback/?locales=en-US'):
    reqs = requests.get(url)
    resps = reqs.json()
    numSpam = 0
    numTotal = resps['count']
    for resp in resps['results']:
        probability = sh.classify([ x for x in re.split('[ \n\r.,?!]', resp['description']) if x != ''])
        if probability > THRESHHOLD:
            numSpam += 1
            resp['spam'] = True
        else:
            resp['spam'] = False
    file_name = 'analyzed-api-data' + str(datetime.now()) + '.json'
    print 'writing to {}'.format(file_name)
    f = open(file_name, 'w')
    json.dump(resps, f)
    print '{} api responses anaylzed.'.format(numTotal)
    print 'Tagged Spam: {} ({}%)'.format(numSpam, percent(numSpam, numTotal))
    print 'Tagged Ham: {} ({}%)'.format(numTotal - numSpam,
        percent(numTotal - numSpam, numTotal))

def test_on_sumo_data_from_mythmons_laptop(url='http://10.252.25.122:8900/api/1/questions?locale=en-US'):
    reqs = requests.get(url)
    resps = reqs.json()
    numSpam = 0
    numTotal = resps['count']
    for resp in resps['results']:
        if not resp['spam']:
            continue
        probability = sh.classify(re.split('[ \n\r.,?!]', resp['content']))
        if probability > THRESHHOLD:
            numSpam += 1
            resp['spam'] = True
        else:
            resp['spam'] = False
    file_name = 'sumo-analyzed-api-data' + str(datetime.now()) + '.json'
    print 'writing to {}'.format(file_name)
    f = open(file_name, 'w')
    json.dump(resps, f)
    print '{} sumo api responses anaylzed.'.format(numTotal)
    print 'Tagged Spam: {} ({}%)'.format(numSpam, percent(numSpam, numTotal))
    print 'Tagged Ham: {} ({}%)'.format(numTotal - numSpam,
        percent(numTotal - numSpam, numTotal))

if __name__ == '__main__':
    sh = Spicedham()
    train_on_api_like_data("jcorpus_newest.json")
    train_on_api_like_data("jcorpus_new.json")
    train_on_api_like_data("jcorpus.json")
    test_file("jcorpus_newest.json")
    test_file("jcorpus_new.json")
    test_file("jcorpus.json")
    #test_on_api_data()
