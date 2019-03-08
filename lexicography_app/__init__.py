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
        result = find_candidates(request.args.get('lemma', type=str), request.args.get('lang', type=int))
    return render_template('search.html', result=result)


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
        result = process_entry(lemma, pos, source, target)
        examples = sample_examples(lemma, pos, source)
        return render_template('entry.html',
                               word={'lemma': lemma,
                                     'pos': pos},
                               examples=examples)
    return render_template('search.html', result=None)


def process_entry(lemma, pos, source, target):
    senses = [i.id for i in Dictionary.query.filter(Dictionary.lemma == lemma,
                                                    Dictionary.lang == source,
                                                    Dictionary.pos == pos).all()]
    return senses


def find_pair_senses(id_sense, target):
    pass


def sample_examples(lemma, pos, source):
    item = Dictionary.query.filter(Dictionary.lemma == lemma,
                                   Dictionary.lang == source,
                                   Dictionary.pos == pos).first().id
    align = defaultdict(lambda: [[], []])
    aligns = Alignment.query.filter(Alignment.id_lemma_right == item).limit(10).all()
    for i in aligns:
        align[i.id_sent][0].append(i.id_left)
        align[i.id_sent][1].append(i.id_right)
    ids = list(align.keys())
    sentences = Examples.query.filter(Examples.id.in_(ids)).all()
    #print(sentences)
    return sentences

def group_translations():
    pass