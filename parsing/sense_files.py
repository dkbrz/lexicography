import sys
import os
import re
import numpy as np
import adagram
import multiprocessing
from functools import partial
import warnings
import argparse
warnings.filterwarnings("ignore")

WINDOW_SIZE = 5


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
    parser = argparse.ArgumentParser(description='Parsing corpus using UDPipe.')
    parser.add_argument('lang_1', type=str, help='name of the language to parse as in downloaded corpus \
            (the name must match the .txt file name from the corpus)')
    parser.add_argument('lang_2', type=str, help='name of the second language in pair as in downloaded corpus \
                (the name must match the .txt file name from the corpus)')
    parser.add_argument('vm', type=str, help='Adagram model')
    args = parser.parse_args()
    lang_1 = args.lang_1
    lang_2 = args.lang_2
    vm = args.vm

    folder = '../languages/' + lang_1 + '_' + lang_2 + '/' + lang_1
    if not os.path.isdir(folder):
        folder = '../languages/' + lang_2 + '_' + lang_1 + '/' + lang_1  # where small files with lemma_pos
    folder_sense = folder + '/' + lang_1 + '_sense'  # new folder for disambiguated files
    folder += '/' + lang_1 + '_lemma_pos'

    vm = adagram.VectorModel.load(vm)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'lemma_pos' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]), reverse=True)

    pool = multiprocessing.Pool(8)
    if not os.path.exists(folder_sense):
        os.mkdir(folder_sense)
    partial_sense = partial(sense_file, model=vm, folder=folder, folder_sense=folder_sense, window=WINDOW_SIZE)
    for i in pool.imap(partial_sense, files):
        print(i)


if __name__ == "__main__":
    main()
