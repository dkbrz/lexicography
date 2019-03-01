import re
import os
import sys


def main():
    folder = sys.argv[1]
    folder_second = sys.argv[2]
    # lang = sys.argv[3]
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'txt' in f]
    files.sort(key=lambda x: int(re.findall('[0-9]+', x)[0]))
    print('Joining files...')
    for file in files:
        with open('{}/{}'.format(folder, file), 'r') as f_r, open('{}/train.txt'.format(folder_second), 'a') as f_w:
            info = f_r.read()
            f_w.write(info)


if __name__ == "__main__":
    main()
