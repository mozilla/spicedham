import os
import re
import json
from datetime import datetime
from subprocess import check_output

import spicedham


def get_data_set():
    with open('responses.json', 'r') as f:
        return json.load(f)


def train():
    train_on_file('jcorpus_newest.json')
    train_on_file('jcorpus_new.json')
    train_on_file('jcorpus.json')


def train_on_file(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    for response in data['results']:
        spicedham.train('description', process_response(response),
                        response['spam'])
        spicedham.train('user_agent', process_response(response),
                        response['spam'])


def classify():
    with open('responses.json', 'r') as f:
        responses = json.load(f)
    return {(result['id'], spicedham.classify(tag,
             process_response(result)))
            for result in responses['results']
            for tag in ['user_agent', 'description']}

def process_user_agent(user_agent):
    return re.sub('[^A-Za-z]+', '', process_response(user_agent))


def process_response(response):
    return filter(lambda x: x != '',
                  re.split(' \n\r.,', response['description']))


def diff_against_previous(data, current_run_name):
    commit_hash = check_output(['git', 'rev-parse', 'HEAD'])
    with open('spicedham-config.json', 'r') as f:
        config_values = f.read()
    build_set = lambda x: {result for result in x}
    last_run_data, last_run = get_last_run_data()
    prev_data = build_set(last_run_data)
    newly_detected = data - prev_data
    fell_out = prev_data - data
    diff = {
        'commit_hash': commit_hash,
        'diffed_files': [last_run, current_run_name],
        'num_fell_out': len(fell_out),
        'num_newly_detected': len(newly_detected),
        'config_values': config_values,
        'fell_out': list(fell_out),
        'newly_detected': list(newly_detected),
    }
    with open('diff-' + current_run_name + '-' + last_run, 'w') as f:
        json.dump(diff, f)


def get_last_run_data():
    prev_runs = sorted(filter(lambda x: x.startswith('analyzed-data-'),
                       os.listdir('.')))
    try:
        last_run = prev_runs[0]
        with open(last_run, 'r') as f:
            last_run_data = json.load(f)
        last_run_data = {tuple(x) for x in last_run_data['data']}
        return (last_run_data, last_run)
    except IndexError:
        return ([], '')


def output_file(data, name):
    with open(name, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    spicedham.load_plugins()
    print 'training...'
    train()
    print 'classifying...'
    data = classify()
    print 'analyzing...'
    current_run_name = 'analyzed-data-' + str(datetime.now()) + '.json'
    diff_against_previous(data, current_run_name)
    print 'writing out the results...'
    output_file({'data': map(list, data)}, current_run_name)
    print 'done!'
