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
    if request.args:
        result = find_candidates(request.args.get('lemma', type=str), request.args.get('source', type=int))
    return render_template('search.html', result=result, target=request.args.get('target', type=int))


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
                                     'pos': pos},
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
    for i in senses:
        result[i[0]] = process_one_sense(i[1], target, reversed=reversed)
    return result    #senses = translations_for_one_sense(senses[0], reversed=False)
    #result = {i[0]:[i[1], 0], {}]}


def get_examples(left, right):
    align = defaultdict(lambda: [[], []])
    aligns = Alignment.query.filter(and_(Alignment.id_lemma_left == left,
                                         Alignment.id_lemma_right == right)).limit(10).all()
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
        left[i] = '<b>'+left[i]+'</b>'
    left = ' '.join(left)
    for i in alignment[1]:
        right[i] = '<b>' + right[i] + '</b>'
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
