#!/usr/bin/python3
from pathlib import Path
from string import punctuation
import os
from tqdm import tqdm
import sys
import argparse


# to clean text from punctuation
def clean(data):
    path = Path()/args['outdir']/f'{data[1]}'
    with open(path, 'w') as file:
        # to parsing index and line in data[0]
        for index, line in enumerate(data[0].split('\n')):
            if index is 1:
                # to check whether the line is the main sentence
                main_sentence = line.split('.')
                try:
                    file.write(main_sentence[0].translate(
                        str.maketrans('', '', punctuation))+'\n')
                except IndexError:
                    print('index error..')

                for sentence in main_sentence[1:]:
                    file.write(sentence.translate(
                        str.maketrans('', '', punctuation)))
                continue
            file.write(line.translate(
                str.maketrans('', '', punctuation))+'\n')


# argument documentary
arg = argparse.ArgumentParser()
arg.add_argument("indir", help="Directory all crawl file")
arg.add_argument("outdir", help="Directory all clean file")
args = vars(arg.parse_args())


# to check whether directory is exist or not
if os.path.exists(args['indir']):
    print(f'Directory : {args["indir"]}')
    # to take file txt running
    for f in tqdm(Path(args['indir']).glob("*.txt")):
        name = str(f).split('/')
        File = open(f, 'r').read()
        clean([File, name[-1]])
else:
    print("Wrong directory path")
    sys.exit(1)
print('\nDone')
