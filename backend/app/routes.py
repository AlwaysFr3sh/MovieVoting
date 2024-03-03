import random
from flask import Blueprint, request
from .db_utils import query_db
from .rooms import RoomTracker

routes = Blueprint('movies', __name__)

def get_id_range():
  query = "SELECT MAX(id) from movies"
  return query_db(query)

def get_movies(ids: tuple):
  query = "SELECT * FROM movies WHERE id in ({})"
  placeholders = ", ".join(["?" for _ in ids])
  query = query.format(placeholders)
  return query_db(query, ids)

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
  room_key = RoomTracker().create()
  return {"room_key" : room_key}
