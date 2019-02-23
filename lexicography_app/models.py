from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Sentences(db.Model):
    __tablename__ = 'sentences'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    sentence_1 = db.Column('sentence_1', db.Text(4294967295))
    sentence_2 = db.Column('sentence_2', db.Text(4294967295))
    #name = db.Column('name', db.Text)


class Dictionary1(db.Model):
    __tablename__ = 'dictionary_1'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    lemma = db.Column('lemma', db.Text)


class Dictionary2(db.Model):
    __tablename__ = 'dictionary_2'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    lemma = db.Column('lemma', db.Text)


class Alignment(db.Model):
    __tablename__ = 'alignment'

    id = db.Column('id', db.Integer,
                   primary_key=True, autoincrement=True)
    id_sent = db.Column('id_sent', db.Integer, db.ForeignKey('sentences.id'))
    ind_token_1 = db.Column('ind_token_1', db.Integer)
    ind_token_2 = db.Column('ind_token_2', db.Integer)
    id_lemma_1 = db.Column('id_lemma_1', db.Integer)
    id_lemma_2 = db.Column('id_lemma_2', db.Integer)
