from datetime import datetime
import copy
from collections import defaultdict
import functools
import gzip
import json
import math
import os
import random
import re
import time
import uuid
import xlsxwriter
import adagram

from functools import wraps, update_wrapper
from sqlalchemy import func, select, and_
from werkzeug.security import generate_password_hash, check_password_hash

from flask import after_this_request, session, jsonify, current_app, send_from_directory, make_response
from flask import Flask, Response
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import func

from lexicography_app.models import *
from lexicography_app.settings import APP_ROOT, CONFIG, LINK_PREFIX
#from lexicography_app.tables import *

from pymystem3 import Mystem
m = Mystem()
#from pylev import levenschtein
from nltk.tokenize import sent_tokenize


DB = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(CONFIG['USER'], CONFIG['PASSWORD'],
                                             CONFIG['HOST'], CONFIG['PORT'], CONFIG['DATABASE'])

ADAGRAM = {}

for i in os.listdir('./lexicography_app/models/'):
    lang = i.split('.')[0]
    ADAGRAM[lang] = adagram.VectorModel.load('./lexicography_app/models/%s' % i)

print(ADAGRAM)

LANGS = {1: 'en', 2:'ru'}

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['APPLICATION_ROOT'] = APP_ROOT
    app.config['SQLALCHEMY_DATABASE_URI'] = DB
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.secret_key = 'yyjzqy9ffY'
    db.app = app
    db.init_app(app)
    return app


app = create_app()

@app.context_processor
def add_prefix():
    return dict(prefix=LINK_PREFIX)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/search", methods=['GET'])
def search_page():
    result = []
    target=0
    if request.args:
        source = request.args.get('direction', type=str).split('-')[0]
        target = request.args.get('direction', type=str).split('-')[1]
        result = find_candidates(request.args.get('lemma', type=str), source)
    return render_template('search.html', result=result, target=target)


def find_candidates(lemma, lang):
    result = Dictionary.query.filter(Dictionary.lemma == lemma, Dictionary.lang == lang).all()
    result = [x for x in sorted(set((i.lemma, i.pos, i.lang) for i in result))]
    return result


@app.route("/entry", methods=['GET'])
def entry():
    if request.args:
        lemma = request.args.get('lemma', type=str)
        pos = request.args.get('pos', type=str)
        source = request.args.get('source', type=int)
        target = request.args.get('target', type=int)
        reverse = bool(get_reverse(source, target))
        print(reverse)
        result = process_entry(lemma, pos, source, target, reverse)
        return render_template('entry.html',
                               word={'lemma': lemma,
                                     'pos': pos,
                                     'source': source,
                                     'target': target},
                               examples=result)
    return render_template('search.html', result=None)


def get_reverse(source, target):
    reverse = Pairs.query.filter(Pairs.id_left == source, Pairs.id_right == target).one().is_reversed
    return reverse


def process_entry(lemma, pos, source, target, reversed):
    senses = [(i.sense, i.id,) for i in Dictionary.query.filter(Dictionary.lemma == lemma,
                                                                Dictionary.lang == source,
                                                                Dictionary.pos == pos).all()]
    result = {}
    try:
        probabilities = ADAGRAM[LANGS[source]].word_sense_probs('{}_{}'.format(lemma, pos))
    except:
        probabilities = []
    for i in senses:
        #neighbors = ADAGRAM[LANGS[source]].sense_neighbors('{}_{}'.format(lemma, pos), i[0])
        neighbors = get_neighbors(source, lemma, pos, i)
        result[i[0]] = {'prob': round(probabilities[i[0]][1], 5), 'neighbors': neighbors, 'sense': i[0], 'id':i[1]}
        result[i[0]]['translations'] = process_one_sense(i[1], target, reversed=reversed)
    result = [result[item] for item in sorted(result, key=lambda x: result[x]['prob'], reverse=True)]
    return result


def get_neighbors(source, lemma, pos, sense):
    neighbors = ADAGRAM[LANGS[source]].sense_neighbors('{}_{}'.format(lemma, pos), sense[0])
    result = [i[0].split('_')+[i[1], i[2]] for i in neighbors]
    return result


def get_examples(left, right, limit=10):
    align = defaultdict(lambda: [[], []])
    aligns = Alignment.query.filter(and_(Alignment.id_lemma_left == left,
                                         Alignment.id_lemma_right == right)).limit(limit).all()
    for i in aligns:
        align[i.id_sent][0].append(i.id_left)
        align[i.id_sent][1].append(i.id_right)
    ids = list(align.keys())
    sentences = Examples.query.filter(Examples.id.in_(ids)).all()
    result = []
    for i in sentences:
        item = prettify(i, align[i.id])
        result.append(item)
    return result


def prettify(pair, alignment):
    left = pair.sent_left.split()
    right = pair.sent_right.split()
    for i in alignment[0]:
        left[i] = '<b class="align">'+left[i]+'</b>'
    left = ' '.join(left)
    for i in alignment[1]:
        right[i] = '<b class="align">' + right[i] + '</b>'
    right = ' '.join(right)
    return left, right


def translations_for_one_sense(id_sense, reversed=False):
    if not reversed:
        n_occurences = db.func.count(Alignment.id)
        translations = db.session.query(n_occurences,
                                        Alignment.id_lemma_right,
                                       )\
            .filter(Alignment.id_lemma_left == id_sense)\
            .group_by(Alignment.id_lemma_right)\
            .having(n_occurences >= 50)\
            .order_by(db.desc(db.func.count(Alignment.id))).all()
    else:

        n_occurences = db.func.count(Alignment.id)
        translations = db.session.query(n_occurences,
                                        Alignment.id_lemma_left,
                                        ) \
            .filter(Alignment.id_lemma_right == id_sense)\
            .group_by(Alignment.id_lemma_left)\
            .having(n_occurences >= 50)\
            .order_by(db.desc(db.func.count(Alignment.id))).all()
    return translations


def process_one_sense(id_sense, target, reversed):
    candidates = translations_for_one_sense(id_sense, reversed=reversed)
    candidates = [[Dictionary.query.get(i[1]), i[0]] for i in candidates if Dictionary.query.get(i[1]).lang == target]
    result = {}
    for i in candidates:
        if not reversed:
            examples = get_examples(id_sense, i[0].id)
        else:
            examples = get_examples(i[0].id, id_sense)
        result[i[0].id] = [i, examples]
    result = [result[i] for i in sorted(result, key=lambda x: result[x][0][1], reverse=True)]
    return result


@app.route("/examples", methods=['GET'])
def full_examples():
    if request.args:
        source = request.args.get('source', type=int)
        target = request.args.get('target', type=int)
        reverse = bool(get_reverse(source, target))
        if not reverse:
            id_left = request.args.get('id_source', type=int)
            id_right = request.args.get('id_target', type=int)
        else:
            id_right = request.args.get('id_source', type=int)
            id_left = request.args.get('id_target', type=int)
        #print(source, target, id_left, id_right)
        all_examples = get_examples(id_left, id_right, limit=1000)
        return render_template('examples.html', examples=all_examples)
    return render_template('examples.html', examples=[])
