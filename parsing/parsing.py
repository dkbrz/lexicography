from model import Model
from conllu import parse


class ParserUDpipe:
    """Parses text using udpipe."""
 
    def __init__(self):
        self.text = ''
        
    def read_file(self, path):
        with open(path, 'r') as file:
            text = file.read()
        return text
    
    def write_file(self, conllu_path, conllu):
        with open(conllu_path, 'w') as file:
            file.write(conllu)
            
    def get_token_sent(self, sent, token='form'):
        return ' '.join([t[token] for t in sent]).strip()
    
    def get_token_string(self, sentences, token='form'):
        token_string = ''
        for sent in sentences:
            token_sent = self.get_token_sent(sent, token=token)
            token_string += token_sent + ' '
        return token_string.strip()
        
    def parsing2conllu(self, path, conllu_path, model):
        print('Parsing', path)
        model = Model(model)
        self.text = self.read_file(path)
        sentences = model.tokenize(self.text)
        for s in sentences:
            model.tag(s)
            model.parse(s)
        conllu = model.write(sentences, "conllu")
        self.write_file(conllu_path, conllu)
        print('Write into', conllu_path)
        
    def lines2tokens(self, CONLLU_FILE, FINAL_FILE, token='form'):
        with open(CONLLU_FILE, 'r') as file_r, open(FINAL_FILE, 'a') as file_w:
            to_parse = ''
            found = False
            for line in file_r:
                if 'SpacesAfter=\\n\\n' not in line and not found:
                    to_parse += line
                if 'SpacesAfter=\\n\\n' in line:
                    to_parse += line
                    found = True
                if found:
                    sentences = parse(to_parse)
                    token_string = self.get_token_string(sentences, token=token)
                    file_w.write(token_string + '\n')
                    to_parse = ''
                    found = False
