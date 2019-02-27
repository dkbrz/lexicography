import sys
import os
from functools import partial
import multiprocessing


def lemma_plus_pos(filename, folder, new_folder):
    """
    :param lemma_file: file (each line - line of lemmas, sep - ' ')
    :param pos_file: file (each line - line of pos, sep - ' ')
    :param output_file: file (each line - lemma1_pos1 lemma2_pos2 ... lemman_posn)
    :return:
    """
    new_filename = filename.replace('lemma', 'lemma_upostag')
    lemma_file = '{}/{}'.format(folder, filename)
    pos_file = lemma_file.replace('lemma', 'upostag')
    output_file = '{}/{}'.format(new_folder, new_filename)
    with open(lemma_file, 'r') as file_l,\
            open(pos_file, 'r') as file_p,\
            open(output_file, 'a') as file_w:
        for line in file_l:
            line_lemma = line.split()
            line_pos = file_p.readline().split()
            lemma_pos = ' '.join([x + '_' + y for x, y in zip(line_lemma, line_pos)]).strip()
            file_w.write(lemma_pos + '\n')


def main():
    folder = sys.argv[1]
    pool = multiprocessing.Pool(8)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'lemma' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    new_folder = folder + '_lemma_pos'
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    partial_parse = partial(lemma_plus_pos,  folder=folder, new_folder=new_folder)
    for i in pool.imap(partial_parse, files):
        print(i)


if __name__ == "__main__":
    main()
