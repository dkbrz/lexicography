from lxml import etree
import re
import argparse


class CleanCorpus:

    def __init__(self):
        self.TMX_FILE = ''
        self.lang_1 = ''
        self.lang_2 = ''

    def find_langs(self):
        langs = re.search(r'(.+?)-(.+?).tmx', self.TMX_FILE)
        if langs:
            self.lang_1 = langs.group(1)
            self.lang_2 = langs.group(2)
        else:
            self.lang_1 = 'in'
            self.lang_2 = 'out'

    def parse_tmx_opus_file(self, TMX_FILE):
        """
        Write into two files: lang_1.txt and lang_2.txt
        """
        self.TMX_FILE = TMX_FILE
        self.find_langs()
        context = etree.iterparse(self.TMX_FILE, tag='tu')
        context = iter(context)
        with open(self.lang_1 + '.txt', 'a') as file_1, open(self.lang_2 + '.txt', 'a') as file_2:
            for event, elem in context:
                en_ru = elem.findall('tuv')
                en = en_ru[0]
                ru = en_ru[1]
                seg_en = en.find('seg')
                seg_ru = ru.find('seg')
                en_text = seg_en.text
                ru_text = seg_ru.text
                file_1.write(en_text + '\n')
                file_2.write(ru_text + '\n')


def main():
    print('Parsing arguments...')
    parser = argparse.ArgumentParser(description='TMX format to TXT.')
    parser.add_argument('tmx_file', type=str, help='file in tmx format')
    args = parser.parse_args()
    tmx = args.tmx_file
    CC = CleanCorpus()
    CC.parse_tmx_opus_file(tmx)


if __name__ == '__main__':
    main()
