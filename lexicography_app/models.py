from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Examples(db.Model):
    __tablename__ = 'examples'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    sent_left = db.Column('sent_left', db.Text(4294967295))
    sent_right = db.Column('sent_right', db.Text(4294967295))


class Dictionary(db.Model):
    __tablename__ = 'dictionary'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    lang = db.Column('lang', db.Integer)
    lemma = db.Column('lemma', db.Text)
    pos = db.Column('pos', db.Text)
    sense = db.Column('sense', db.Integer)


class Alignment(db.Model):
    __tablename__ = 'alignment'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    id_sent = db.Column('id_sent', db.Integer, db.ForeignKey('sentences.id'))
    id_left = db.Column('id_left', db.Integer)
    id_right = db.Column('id_right', db.Integer)
    id_lemma_left = db.Column('id_lemma_left', db.Integer)
    id_lemma_right = db.Column('id_lemma_right', db.Integer)


class Pairs(db.Model):
    __tablename__ = 'pairs'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    id_left = db.Column('id_left', db.Integer)
    id_right = db.Column('id_right', db.Integer)
    n_examples = db.Column('n_examples', db.Integer)
    is_reversed = db.Column('is_reversed', db.Integer)


class Languages(db.Model):
    __tablename__ = 'langs'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column('name', db.Text)
    n_senses_words = db.Column('n_senses_words', db.Integer)


class OneSense:
    def __init__ (self, x):
        self.id = x
        self.n = 0
        self.synonims = []
        self.translations = []


