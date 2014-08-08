import os
import re
import tarfile
import json
import requests
from datetime import datetime

import spicedham as sh

def setUp(tarball='corpus.tar.gz', test_data_dir='corpus', backup_url='https://dl.dropboxusercontent.com/u/84239013/corpus.tar.gz'):
    if os.path.exists(test_data_dir):
        pass
    elif os.path.exists(tarball):
        tr = tarfile.open(tarball)
        tr.extractall()
        tr.close()
    else:
        r = requests.get(backup_url)
        s = r.read()
        f = open(tarball, 'wb')
        f.write(s)
        setup()
        return


def train_on(dir_name, is_spam):
    print 'training with the belief that everything in {} is spam is {}'.format(
        dir_name, is_spam)
    for file_name in os.listdir(dir_name):
        data = json.load(open(os.path.join(dir_name, file_name)))
        sh.train(re.split('[ .,?!]', data['description']), is_spam)


def test_on_training_data():
    print 'testing against the training data set'
    test_on_data(os.path.join('corpus', 'train'))


def test_on_control_data():
    print 'testing against the control data set'
    test_on_data(os.path.join('corpus', 'control'))

def train_on_api_like_data(file_name='crowd-corpus.json'):
    if os.path.exists(file_name):
        print 'training on the crowd corpus'
        sh.train_bulk(file_name)
    else:
        print 'crowd corpus not found. continuing without it.'

def test_on_data(test_data_dir):
    _test_all_files_in_dir(
        os.path.join(test_data_dir, 'spam'), True)
    _test_all_files_in_dir(
        os.path.join(test_data_dir, 'ham'), False)


def _test_all_files_in_dir(data_dir, should_be_spam):
    test_results = {
        'Total': [],
        'True+': [],
        'False+': [],
        'True-': [],
        'False-': [],
        'Error': [],
    }
    tuning_factor = 0.5
    for filename in os.listdir(data_dir):
        f = open(os.path.join(data_dir,  filename), 'r')
        json_response = json.load(f)
        probability = sh.classify(re.split('[ \n\r.,?!]', json_response['description']))
        test_results['Total'].append(filename)
        if 0.0 > probability > 1.0:
            test_results['Error'].append(filename)
        if should_be_spam:
            if probability > tuning_factor:
                test_results['True+'].append(filename)
            else:
                test_results['False-'].append(filename)
        else:
            if probability < tuning_factor:
                test_results['True-'].append(filename)
            else:
                test_results['False+'].append(filename)
    show_results(test_results)

def show_results(test_results):
    red = '\033[0;31m'
    green = '\033[0;32m'
    nocolor = '\033[0m'
    print test_results['False-']
    print '{} responses analyzed'.format(len(test_results['Total']))
    print 'True positives:  {} ({}%)'.format(len(test_results['True+']),
        percent(len(test_results['True+']), len(test_results['Total'])))
    print 'False negatives: {} ({}%)'.format(len(test_results['False-']),
        percent(len(test_results['False-']), len(test_results['Total'])))
    print 'True negatives:  {} ({}%)'.format(len(test_results['True-']),
        percent(len(test_results['True-']), len(test_results['Total'])))
    print 'False positives: {} ({}%)'.format(len(test_results['False+']),
        percent(len(test_results['False+']), len(test_results['Total'])))
    print 'Errors:          {} ({}%)'.format(len(test_results['Error']),
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
        probability = sh.classify(re.split('[ \n\r.,?!]', resp['description']))
        if probability > 0.5:
            numSpam += 1
            resp['spam'] = True
        else:
            resp['spam'] = False
    file_name = 'analyzed-api-data' + str(datetime.now()) + '.json'
    print 'writing to {}'.format(file_name)
    f = open(file_name, 'w')
    json.dump(resps, f)
    print 'api'
    print '{} api responses anaylzed.'.format(numTotal)
    print 'Tagged Spam: {} ({}%)'.format(numSpam, percent(numSpam, numTotal))
    print 'Tagged Hpam: {} ({}%)'.format(numTotal - numSpam,
        percent(numTotal - numSpam, numTotal))

if __name__ == '__main__':
    setUp()
    train_on(os.path.join('corpus', 'train', 'spam'), True)
    train_on(os.path.join('corpus', 'train', 'ham'), False)
    #train_on_api_like_data()
    test_on_training_data()
    #test_on_control_data()
    test_on_api_data()
