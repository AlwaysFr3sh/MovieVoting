#!/usr/bin/env python3
from flask import Flask
import sys
import sqlite3
import json

app = Flask("changethislater")

def movie(year: str, title: str) -> str:
  con = sqlite3.connect("movies.db") 
  cursor = con.cursor()
  cursor.execute(f"SELECT * FROM movies WHERE title = (?) AND year = (?)", (title, year))
  data = cursor.fetchall()
  columns = [col[0] for col in cursor.description]
  data = [dict(zip(columns, row)) for row in data]
  con.close()
  return json.dumps(data, indent=2)


"""
Bad news, sqlite does not support seeded random, which ruins my plans!!!
instead future me (you) will have to 
"""

def random_movies(count: int):
  con = sqlite3.connect("movies.db")
  cursor = con.cursor()
  #cursor.execute(f"SELECT * FROM movies WHERE id IN (SELECT id from movies ORDER BY RANDOM() LIMIT ?)", (count,))
  # TODO: replace query tuple with randomly generated one of length: count
  cursor.execute(f"SELECT * FROM movies WHERE id IN ({'?, ' * (count - 1) + '?'})", (1, 2, 3, 4, 5, 6, 7, 8, 9))
  data = cursor.fetchall()
  columns = [col[0] for col in cursor.description]
  data = [dict(zip(columns, row)) for row in data]
  con.close()
  return json.dumps(data, indent=2)

# TODO: is year necessary?
# should usually only return one entry
# TODO: purge database of NaN entries
@app.route("/movies/<year>/<title>", methods=["GET"])
def get_movies(year: str, title: str):
  return movies(year, title)

#TODO: reject request if no count provided
@app.route("/random", methods=["GET"])
def get_random():
  return random_movies(request.args.get("count"))


if __name__ == "__main__":
  #print(type(movie("2007", "Transformers")).__name__) # pretty cool
  print(random_movies(9))