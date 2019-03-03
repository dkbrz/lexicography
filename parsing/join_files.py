import re
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Parsing corpus using UDPipe.')
    parser.add_argument('lang_1', type=str, help='name of the language to parse as in downloaded corpus \
        (the name must match the .txt file name from the corpus)')
    parser.add_argument('lang_2', type=str, help='name of the second language in pair as in downloaded corpus \
            (the name must match the .txt file name from the corpus)')
    args = parser.parse_args()
    lang_1 = args.lang_1
    lang_2 = args.lang_2
    folder = '../languages/' + lang_1 + '_' + lang_2 + '/' + lang_1
    if not os.path.isdir(folder):
        folder = '../languages/' + lang_2 + '_' + lang_1 + '/' + lang_1
    files = [f for f in os.listdir(folder + '/' + lang_1 + '_lemma_pos') if '.txt' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    train_file = '{}/train.txt'.format(folder)

    print('Joining files...')
    for file in files:
        f = '{}/{}'.format(folder + '/' + lang_1 + '_lemma_pos', file)
        print('Adding file ' + f + '...')
        with open(f, 'r') as f_r,\
                open(train_file, 'a') as f_w:
            info = f_r.read().rstrip()
            f_w.write(info+'\n')
    print('File ' + train_file + ' is ready.')


if __name__ == "__main__":
    main()
