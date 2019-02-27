import sys
import os
import re
import subprocess
import numpy as np
import adagram
import multiprocessing
from functools import partial

WINDOW_SIZE = 7


def find_context(ind, words, window=WINDOW_SIZE):
    if ind - window < 0:
        start = 0
    else:
        start = ind - window

    if ind + window > len(words):
        end = len(words) + 1
    else:
        end = ind + window + 1

    left = words[start:ind]
    right = words[ind + 1:end]
    return left + right


def find_sense(word, context, model):
    try:
        probs = model.disambiguate(word, context)
        sense = np.argmax(probs, axis=0)
    except:
        sense = 0
    return str(sense)


def sense_line(line, model, window=WINDOW_SIZE):
    new_line = ''
    words = line.split()
    for ind, word in enumerate(words):
        context = find_context(ind, words, window=window)
        sense = find_sense(word, context, model=model)
        word = word + '_' + sense
        new_line += word + ' '
    return new_line.strip()


def sense_file(file, model, folder, folder_sense, window=WINDOW_SIZE):
    with open('{}/{}'.format(folder, file), 'r') as file_r, open('{}/sense_'.format(folder_sense) + file, 'a') as file_w:
        for line in file_r:
            new_file = sense_line(line, model=model, window=window)
            file_w.write(new_file + '\n')
    return file


def main():
    folder = sys.argv[1]
    folder_sense = sys.argv[2]
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'txt' in f]
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
    for file in files:
        with open('{}/{}'.format(folder, file), 'r') as f_r, open('{}/train.txt'.format(folder), 'a') as f_w:
            info = f_r.read()
            f_w.write(info)

    subprocess.call([
        'adagram-train',
        '{}/train.txt'.format(folder),
        'out.pkl',
        '--min-freq', 100,
        '--dim', 300,
        '--epochs', 5,
        '--workers', 8,
        '--window', 3
    ])

    vm = adagram.VectorModel.load("out.pkl")
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
