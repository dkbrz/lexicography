import argparse
import os
import re
import subprocess
import adagram
import multiprocessing
from functools import partial

WINDOW_SIZE = 5


def create_folder(name):
    print('Creating folder ' + name)
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        print('You have already have this folder.')


def main():
    parser = argparse.ArgumentParser(description='Parsing corpus using UDPipe.')
    parser.add_argument('lang_1', type=str, help='name of the language to parse as in downloaded corpus \
        (the name must match the .txt file name from the corpus)')
    parser.add_argument('lang_2', type=str, help='name of the second language in pair as in downloaded corpus \
            (the name must match the .txt file name from the corpus)')
    parser.add_argument('--train', type=str, help='train new model?', dest='train_bool',
                        action='store_true', default=False)
    args = parser.parse_args()
    lang_1 = args.lang_1
    lang_2 = args.lang_2
    train_bool = args.train_bool
    folder = '../languages/' + lang_1 + '_' + lang_2 + '/' + lang_1
    if not os.path.isdir(folder):
        folder = '../languages/' + lang_2 + '_' + lang_1 + '/' + lang_1
    files = [f for f in os.listdir(folder + '/' + lang_1 + '_lemma_pos') if '.txt' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    train_file = '{}/train.txt'.format(folder)

    if train_bool:
        print('Joining files...')
        for file in files:
            f = '{}/{}'.format(folder + '/' + lang_1 + '_lemma_pos', file)
            print('Adding file ' + f + '...')
            with open(f, 'r') as f_r,\
                    open(train_file, 'a') as f_w:
                info = f_r.read().rstrip()
                f_w.write(info + '\n')
        print('File ' + train_file + ' is ready.')

        print('Training model...')
        subprocess.call([
            'adagram-train',
            '{}'.format(train_file),
            '{}/{}.pkl'.format(folder, lang_1),
            '--min-freq', '100',
            '--dim', '300',
            '--workers', '8',
            '--window', '5'
        ])
    vm = adagram.VectorModel.load('{}/{}.pkl'.format(folder, lang_1))
    files = [f for f in os.listdir(folder + '/' + lang_1 + '_lemma_pos')]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    sense_folder = folder + '/' + lang_1 + '_sense'
    create_folder(sense_folder)
    partial_parse = partial(model=vm, folder=folder, folder_sense=sense_folder, window=WINDOW_SIZE)
    pool = multiprocessing.Pool(8)
    for i in pool.imap(partial_parse, files):
        print(i)


if __name__ == "__main__":
    main()
