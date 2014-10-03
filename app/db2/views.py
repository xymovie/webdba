from __future__ import print_function
import json
from flask import render_template, current_app, Response
from flask.ext.login import login_required
from . import db2
from .db2sql import DB2

@db2.route('/')
@login_required
def index():
    colnames = []
    rows = []
    return render_template('db2/index.html')

@db2.route('/entries')
@login_required
def entries():
    colnames = []
    rows = []
    with DB2(current_app) as db2:
        colnames, rows = db2.snapappl()
    
    return render_template('db2/entries.html', colnames = colnames, rows = rows) 
