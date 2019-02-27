import sys
import os
import re
import subprocess
import numpy as np
import adagram
import multiprocessing
from functools import partial

WINDOW_SIZE = 5


def main():
    folder = sys.argv[1]
    folder_sense = sys.argv[2]
    lang = sys.argv[3]
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'txt' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    print('Joining files...')
    for file in files:
        with open('{}/{}'.format(folder, file), 'r') as f_r, open('{}/train.txt'.format(folder), 'a') as f_w:
            info = f_r.read()
            f_w.write(info)
    print('Training model...')
    subprocess.call([
        'adagram-train',
        '{}/train.txt'.format(folder),
        '{}.pkl'.format(lang),
        '--min-freq', '100',
        '--dim', '300',
        '--workers', '8',
        '--window', '5'
    ])

    vm = adagram.VectorModel.load('{}.pkl'.format(lang))
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'lemma_upostag' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    if not os.path.exists(folder_sense):
        os.mkdir(folder_sense)
    partial_parse = partial(model=vm, folder=folder, folder_sense=folder_sense, window=WINDOW_SIZE)
    pool = multiprocessing.Pool(8)
    for i in pool.imap(partial_parse, files):
        print(i)


if __name__ == "__main__":
    main()
