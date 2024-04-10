import sqlite3
from flask import g

def make_dicts(cursor, row):
  return dict((cursor.description[idx][0], value)
              for idx, value in enumerate(row))

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect("movies.db")
    db.row_factory = make_dicts
  return db

def query_db(query, args=(), one=False):
  cursor = get_db().execute(query, args)
  rv = cursor.fetchall()
  cursor.close()
  return (rv[0] if rv else None) if one else rv

def close_db():
  db = getattr(g, '_database', None)
  print("Closing db...", flush=True)
  if db is not None:
    db.close()


"""
def init_db():
  db = get_db()
  with current_app.open_resource("schema.sql") as f:
    db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
"""