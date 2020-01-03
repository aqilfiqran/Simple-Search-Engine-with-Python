#!/usr/bin/python3
import json
import sys
import os
from pathlib import Path
import argparse

# argument documentary
arg = argparse.ArgumentParser()
arg.add_argument("indexfile", help="path for index file")
arg.add_argument("linkfile", help="path for link file")
arg.add_argument("-t", "--top", help="top document result",
                 type=int, required=False)
arg.add_argument('search', nargs='+',
                 help='searh word')
args = vars(arg.parse_args())

# make hash
listterm, query, result = dict(), dict(), dict()
# read index file and put to hash
with open(args['indexfile'], 'r') as file:
    file = file.read()
    for lines in file.split('\n'):
        line = lines.split(' ')
        listterm[line[0]] = dict()
        for col in line[1:]:
            datacol = col.split(':')
            listterm[line[0]][datacol[0]] = datacol[1]

# to count duplicate word
for word in args['search']:
    word = word.lower()
    if word in query:
        query[word] += 1
    else:
        query[word] = 1


for word, term in query.items():
    if word not in listterm:
        continue
    # sort doc rank
    index = sorted(listterm[word].items(), key=lambda x: x[1], reverse=True)
    for doc, score in index:
        if score is '0':
            break
        if doc in result:
            result[doc] += float(score) * term
        else:
            result[doc] = float(score)

results = sorted(result.items(), key=lambda x: x[1], reverse=True)
outjson = []

# doc top rank
top = args['top'] if args['top'] is not None else len(results)

i = 0
# make json
with open(args['linkfile'], 'r') as link:
    links = link.read().split('\n')
    for doc, score in results:
        index = doc.split('.')
        index = index[0].split('data')
        if score is '0' or int(top) is i:
            break

        try:
            outjson.append({
                'doc': doc,
                'score': score,
                'url': links[int(index[1])-1],
            })
            i += 1
        except ValueError:
            pass

# output json
print(json.dumps(outjson))
