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
    folder = '../languages/' + lang_1 + '_' + lang_2 + '/'
    files = [f for f in os.listdir(folder + '/' + lang_1 + '_sense') if '.txt' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    train_file = '{}/{}_align.txt'.format(folder, lang_1)

    print('Joining files...')
    for key, file in enumerate(files):
        f = '{}/{}'.format(folder + '/' + lang_1 + '_sense', file)
        print('Adding file ' + f + '...')
        with open(f, 'r') as f_r,\
                open(train_file, 'a') as f_w:
            info = f_r.read().rstrip()
            f_w.write(info)
            if key != len(files)-1:
                f_w.write('\n')
    print('File ' + train_file + ' is ready.')


if __name__ == "__main__":
    main()
