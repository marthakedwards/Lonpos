#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, g
import sqlite3, os, sys
import json

con = sqlite3.connect('db.sqlite3')

# App configuration
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'db.sqlite3')
))

# Database connection access
def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv

def get_db():
  if not hasattr(g, 'sqlit_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

@app.teardown_appcontext
def close_db(exception):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()

def init_db():
  db = get_db()
  with app.open_resource('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
  import lonpos
  db.commit()

@app.cli.command('initdb')
def initdb_command():
  init_db()
  print('Initialized the database.')

# URL routing and template rendering
@app.route('/')
def flat():
  with con:
    cur = con.cursor()
    cur.execute("select * from coord where board_id = " + 
      "(select board_id from coord order by random() limit 1);")
    rows = cur.fetchall()
    return render_template('flat.html', coordinates=json.dumps(rows))

@app.route('/pyramid')
def pyramid():
  return 'pyramid!'

@app.route('/about')
def about():
  return 'about!'
