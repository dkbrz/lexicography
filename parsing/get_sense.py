import sys
import os
import subprocess
import numpy as np
import adagram


def find_context(ind, words, window=5):
    if ind - window < 0:
        start = 0
    else:
        start = ind - window

    if ind + window > len(words):
        end = len(words) + 1
    else:
        end = ind + window + 1

    left = words[start:ind]
    right = words[ind + 1:end]
    return left + right


def find_sense(word, context, model):
    try:
        probs = model.disambiguate(word, context)
        sense = np.argmax(probs, axis=0)
    except:
        sense = 0
    return str(sense)


def sense_line(line, model, window=5):
    new_line = ''
    words = line.split()
    for ind, word in enumerate(words):
        context = find_context(ind, words, window=window)
        sense = find_sense(word, context, model=model)
        word = word + '_' + sense
        new_line += word + ' '
    return new_line.strip()


def sense_file(file, model, folder, folder_sense, window=5):
    with open('{}/{}'.format(folder, file), 'r') as file_r, open('{}/sense_'.format(folder_sense) + file, 'a') as file_w:
        for line in file_r:
            new_file = sense_line(line, model=model, window=window)
            file_w.write(new_file + '\n')


def main():
    folder = sys.argv[1]
    folder_sense = sys.argv[2]
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'txt' in f]
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
    for file in files:
        with open('{}/{}'.format(folder, file), 'r') as f_r, open('{}/train.txt'.format(folder), 'a') as f_w:
            info = f_r.read()
            f_w.write(info)

    subprocess.call(['adagram-train', '{}/train.txt'.format(folder, file), 'out.pkl'])

    vm = adagram.VectorModel.load("out.pkl")
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and 'lemma_upostag' in f]
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
    if not os.path.exists(folder_sense):
        os.mkdir(folder_sense)
    for f in files:
        sense_file(f, vm, folder, folder_sense, window=5)


if __name__ == "__main__":
    main()
