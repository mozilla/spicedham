import os
import shutil
import json
from datetime import datetime

import psycopg2

DB_URL = os.environ['DATABASE_URL']

def get_dump_from_db():
    connection = psycopg2.connect(DB_URL)
    cur = connection.cursor()
    cur.execute('select is_spam, json from responses where is_spam!=3;')
    classified = cur.fetchall()
    api_like = {
        'count': len(classified),
        'results': []
    }
    for is_spam, jsresponse in classified:
        response = json.loads(jsresponse)
        if is_spam == 1:
            response['spam'] = True
        else:
            response['spam'] = False
        api_like['results'].append(response)
    api_like_json = json.dumps(api_like)
    file_name = 'crowd-corpus' + str(datetime.now()) + '.json'
    with open(file_name, 'w') as f:
        f.write(api_like_json)
    file_name = 'crowd-corpus.json'
    with open(file_name, 'w') as f:
        f.write(api_like_json)

get_dump_from_db()
