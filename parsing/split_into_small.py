import os
import argparse

LINES_PER_FILE = 250000


def split_bigfile(path_bigfile, new_folder, lang, lines_per_file=LINES_PER_FILE):
    """
    :param file: (txt format) - file to split
    :param folder: where small files will be saved
    :param lines_per_file: (int) - number of lines in small file
    """
    smallfile = None
    try:
        with open(path_bigfile) as bigfile:
            k = 0
            for i, line in enumerate(bigfile):
                if i % lines_per_file == 0:
                    if smallfile:
                        smallfile.close()
                    small_filename = new_folder + '/{}_raw_{}.txt'.format(lang, str(k))
                    smallfile = open(small_filename, "w")
                    k += 1
                smallfile.write(line + '\n')
            if smallfile:
                smallfile.close()
    except:
        print('Check if you have big file in folder data')


def create_folder(name):
    print('Creating folder ' + name)
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        print('You have already have this folder.')


def splitting(folder, lang):
    print('Splitting the big file for ' + lang)
    raw_folder = folder + '/' + lang + '_raw'
    create_folder(raw_folder)
    split_bigfile('../data/' + lang + '.txt', raw_folder, lang, lines_per_file=LINES_PER_FILE)
    print('Big file for ' + lang + ' is splitted.')


def main():
    print('Parsing arguments...')
    parser = argparse.ArgumentParser(description='Parsing corpus using UDPipe.')
    parser.add_argument('lang_1', type=str, help='name of the first language as in downloaded corpus \
    (the name must match the .txt file name from the corpus)')
    parser.add_argument('lang_2', type=str, help='name of the second language as in downloaded corpus \
    (the name must match the .txt file name from the corpus)')
    args = parser.parse_args()
    lang_1 = args.lang_1
    lang_2 = args.lang_2
    print('Parsed languages: language 1 - ' + lang_1 + ', language 2 - ' + lang_2)

    # Create folders for languages
    create_folder('../languages')
    folder_for_2 = '../languages/' + lang_1 + '_' + lang_2
    create_folder(folder_for_2)
    folder_1 = folder_for_2 + '/' + lang_1
    folder_2 = folder_for_2 + '/' + lang_2
    create_folder(folder_1)
    create_folder(folder_2)

    # Split into small files
    splitting(folder_1, lang_1)
    splitting(folder_2, lang_2)


if __name__ == '__main__':
    main()
