import random
from flask import Blueprint, request, jsonify, send_file
from .db_utils import query_db
import requests
import io

from .rooms import RoomTracker
from .games import GameService

routes = Blueprint('movies', __name__)

class RouteException(Exception):
  status_code = 400

  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = message
    if status_code is not None:
      self.status_code = status_code
    self.payload = payload
  
  def to_dict(self):
    ret = dict(self.payload or ())
    ret["message"] = self.message
    return ret

@routes.errorhandler(RouteException)
def handle_exception(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response

# TODO: scheduled for demolition
@routes.route('/create_room', methods=['POST'])
def create_room():
  #room_key = RoomTracker().create()
  room_key = GameService().create_game()
  return {"room_key" : room_key}

# TODO: do i need to escape(data)???
# TODO: Doesnt work, make it work
@routes.route("/movies/<string:game_pin>", methods=["GET"])
def movies(game_pin):
  limit = 5
  username = request.args.get("username") or None
  if username is None: raise RouteException("Missing Argument <username>", status_code=400)
  # Do caching of movie data if we ever feel like it (probably when we move to spring boot) 
  movies = GameService().get_movies(game_pin, username, limit)
  return movies
  
# TODO: should game pin and / or movie id be like this url/<this> or like this /url?this=this?
#       consider this for the movies endpoint too
@routes.route("/posters/<string:game_pin>/<string:movie_id>", methods=["GET"])
def posters(game_pin, movie_id):
  # validate game pin and stuff
  username = request.args.get("username") or None
  # TODO: we can either get api key from ENV var, load from config at startup or read from file for every request like this (dumb I think)
  from seed import omdb_key
  r = requests.get(f"http://img.omdbapi.com/?apikey={omdb_key()}&i=tt{movie_id}&h=600")
  # TODO: should I return json or html for error here?
  if r.status_code != 200: raise RouteException("insert an error msg here", status_code=r.status_code)
  return send_file(
    io.BytesIO(r.content),
    mimetype="image/png"
  )


