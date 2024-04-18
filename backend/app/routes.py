import random
from flask import Blueprint, request
from .db_utils import query_db

from .rooms import RoomTracker
from .games import GameService

routes = Blueprint('movies', __name__)

def get_id_range():
  query = "SELECT MAX(id) from movies"
  return query_db(query)

def get_movies(ids: tuple):
  query = "SELECT * FROM movies WHERE id in ({})"
  placeholders = ", ".join(["?" for _ in ids])
  query = query.format(placeholders)
  return query_db(query, ids)


"""
TODO: 

store a the random seed in the database on 
game creation

instead of doing what we do now

do an ORDER BY SIN(id + seed) query to get our random results (consistently)

Here is the forum posts referenced for this idea, delete this comment when implemented

https://www.sqlite.org/forum/forumpost/e2216583a4
https://stackoverflow.com/questions/1253561/sqlite-order-by-rand/75089040#75089040

"""
@routes.route("/movies", methods=["GET"])
def movies():
  seed = request.args.get("seed")
  r = random.Random(seed)
  id_range = get_id_range()[0]["MAX(id)"]
  ids = r.sample(range(1, id_range), 5)
  movies = get_movies(ids)
  return movies 

@routes.route('/create_room', methods=['POST'])
def create_room():
  #room_key = RoomTracker().create()
  room_key = GameService().create_game()
  return {"room_key" : room_key}
