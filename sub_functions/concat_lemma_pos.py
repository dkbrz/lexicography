import sys

def lemma_plus_pos(lemma_file, pos_file, output_file):
    """

    :param lemma_file: file (each line - line of lemmas, sep - ' ')
    :param pos_file: file (each line - line of pos, sep - ' ')
    :param output_file: file (each line - lemma1_pos1 lemma2_pos2 ... lemman_posn)
    :return:
    """
    with open(lemma_file, 'r') as file_l, open(pos_file, 'r') as file_p, open(output_file, 'a') as file_w:
        for line in file_l:
            line_lemma = line.split()
            line_pos = file_p.readline().split()
            lemma_pos = ' '.join([x + '_' + y for x, y in zip(line_lemma, line_pos)]).strip()
            file_w.write(lemma_pos + '\n')


if __name__ == "__main__":
    lemma_file = sys.argv[1]
    pos_file = sys.argv[2]
    output_file = sys.argv[3]
    lemma_plus_pos(lemma_file, pos_file, output_file)
