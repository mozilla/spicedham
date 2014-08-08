import json

should_be_spam = [ 
4545620,
4545503,
4545489,
4545483,
4545455,
4545408,
4546684,
4547509,]
should_be_ham =[
4545606,
4546702,
4547479,
4547475,
4547417,
]
nix = [
4545607,
4545704,
4545336,
4545508,
4545339,
4546639,
4546661,
4547410,
4545556,
4546536,
]

def filter():
    with open('crowd-corpus-edited.json', 'r+') as f:
        j = json.load(f)
        for i in j['results']:
            if i['id'] in should_be_spam:
                i['spam'] = True
            elif i['id'] in should_be_ham:
                i['spam'] = False
        j = [i for i in j['results'] if i['id'] not in nix]
        j = json.dumps(j)
        f.write(j)

filter()
