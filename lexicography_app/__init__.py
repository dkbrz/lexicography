from datetime import datetime
import copy
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


DB = CONFIG

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
#app.route = prefix_route(app.route, '/foklore/')
# db.create_all()
# app.app_context().push()
#login_manager.init_app(app)

@app.context_processor
def add_prefix():
    return dict(prefix=LINK_PREFIX)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
