import sys
import os

def split_file(file, folder, lines_per_file):
    """
    input:
        file (txt format) - file to split
        folder - where small files will be saved
        lines_per_file (int) - number of lines in small file
    example:
        python split_into_small_files.py big_file.txt test 10000
    """
    curr_dir = os.getcwd()
    new_folder = curr_dir + '/' + folder
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    smallfile = None
    with open(file) as bigfile:
        for i, line in enumerate(bigfile):
            if i % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = new_folder + '/{}.txt'.format(i + lines_per_file)
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()


if __name__ == "__main__":
    file = sys.argv[1]
    folder = sys.argv[2]
    lines_per_file = int(sys.argv[3])
    split_file(file, folder, lines_per_file)
