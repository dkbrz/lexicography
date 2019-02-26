from functools import partial
import sys
import os
import multiprocessing
from parsing import ParserUDpipe
from conllu import parse


def parsing(filename, MODEL, folder, new_folder):
    print(filename)
    parser = ParserUDpipe()
    parser.parsing2conllu('./{}/{}'.format(folder, filename), '{}/conllu_{}'.format(new_folder, filename), MODEL)
    return filename


def main():
    folder = sys.argv[1]
    MODEL = sys.argv[2]
    pool = multiprocessing.Pool(7)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
    new_folder = folder + '_conllu'
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    partial_parse = partial(parsing, folder=folder, MODEL=MODEL, new_folder=new_folder)
    for i in pool.imap(partial_parse, files):
        print(i)


if __name__ == '__main__':
    main()