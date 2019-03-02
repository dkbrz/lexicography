from functools import partial
import re
import os
import multiprocessing
from parsing import ParserUDpipe
import argparse
import shutil


def create_folder(name):
    print('Creating folder ' + name)
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        print('You have already have this folder.')


def lemma_plus_pos(lemma_file):
    print(lemma_file)
    pos_file = re.sub('lemma', 'pos', lemma_file)
    output_file = re.sub('lemma', 'lemma_pos', lemma_file)

    with open(lemma_file, 'r') as file_l,\
            open(pos_file, 'r') as file_p,\
            open(output_file, 'a') as file_w:
        for line in file_l:
            line_lemma = line.split()
            line_pos = file_p.readline().split()
            lemma_pos = ' '.join([x + '_' + y for x, y in zip(line_lemma, line_pos)]).strip()
            file_w.write(lemma_pos + '\n')


def parsing(filename, folder, lang_1, conllu_folder, MODEL):
    print('Filename: ' + filename)
    parser = ParserUDpipe()
    conllu_file = conllu_folder + '/' + filename.replace('raw', 'conllu')
    parser.parsing2conllu('{}/{}_raw/{}'.format(folder, lang_1, filename), conllu_file, MODEL)
    parser.lines2tokens(conllu_file, folder + '/' + lang_1 + '_lemma' + '/' + filename.replace('raw', 'lemma'), token='lemma')
    parser.lines2tokens(conllu_file, folder + '/' + lang_1 + '_token' + '/' + filename.replace('raw', 'token'), token='form')
    parser.lines2tokens(conllu_file, folder + '/' + lang_1 + '_pos' + '/' + filename.replace('raw', 'pos'), token='upostag')
    lemma_plus_pos(folder + '/' + lang_1 + '_lemma' + '/' + filename.replace('raw', 'lemma'))
    return filename


def main():
    print('Parsing arguments...')
    parser = argparse.ArgumentParser(description='Parsing corpus using UDPipe.')
    parser.add_argument('lang_1', type=str, help='name of the language to parse as in downloaded corpus \
    (the name must match the .txt file name from the corpus)')
    parser.add_argument('lang_2', type=str, help='name of the second language in pair as in downloaded corpus \
        (the name must match the .txt file name from the corpus)')
    parser.add_argument('--parse', type=str, help='name of the second language as in downloaded corpus \
            (the name must match the .txt file name from the corpus)')
    parser.add_argument('udpipe_model', type=str, help='directory for model of language')
    args = parser.parse_args()
    lang_1 = args.lang_1
    lang_2 = args.lang_2
    MODEL = args.udpipe_model
    print('Parsed language: ' + lang_1)
    print('Parsed model: ' + MODEL)

    # Parsing with UDPipe
    folder = '../languages/' + lang_1 + '_' + lang_2 + '/' + lang_1
    if not os.path.isdir(folder):
        folder = '../languages/' + lang_2 + '_' + lang_1 + '/' + lang_1
    pool = multiprocessing.Pool(8)
    print('Creating folders for language ' + lang_1)
    conllu_folder = folder + '/' + lang_1 + '_conllu'
    create_folder(conllu_folder)
    lemma_folder = folder + '/' + lang_1 + '_lemma'
    create_folder(lemma_folder)
    token_folder = folder + '/' + lang_1 + '_token'
    create_folder(token_folder)
    pos_folder = folder + '/' + lang_1 + '_pos'
    create_folder(pos_folder)
    lemma_pos_folder = folder + '/' + lang_1 + '_lemma_pos'
    create_folder(lemma_pos_folder)
    files = [f for f in os.listdir(folder + '/' + lang_1 + '_raw')]
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[2]))
    print('Amount of files: ' + str(len(files)))
    partial_parse = partial(parsing, folder=folder, lang_1=lang_1, conllu_folder=conllu_folder, MODEL=MODEL)
    for i in pool.imap(partial_parse, files):
         print(i)
    shutil.rmtree(pos_folder)
    shutil.rmtree(lemma_folder)


if __name__ == '__main__':
    main()
