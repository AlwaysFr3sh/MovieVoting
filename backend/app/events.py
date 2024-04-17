from random import randrange 

import socketio
from flask import current_app

from .rooms import RoomTracker
from .games import GameService

class Namespace(socketio.Namespace):

  def __init__(self, app, namespace=None):
    super().__init__(namespace=namespace)
    self.app = app
  
  def app_context(foo):
    def app_context_wrapper(self, *args, **kwargs):
      with self.app.app_context():
        return foo(self, *args, **kwargs)
    return app_context_wrapper

  def on_connect(self, sid, environ):
    print(f"connected: {sid}")

  @app_context
  def on_disconnect(self, sid):
    rooms_to_leave = [room for room in self.rooms(sid) if room != sid]
    for room in rooms_to_leave:
      room_members = [self.get_username(member['socketid']) for member in GameService().leave_game(sid, room)] 
      self.leave_room(sid, room)
      self.emit('update_lobby', {"members" : room_members}, room=room, skip_sid=sid)
    print(f"Disconnected: {sid}")
  
  @app_context
  def on_join_room(self, sid, data):
    username, room = data["username"], data["room_key"]
    try:
      game = GameService().get_game(room)
      print(game)
      if game['status'] != 0:
        raise Exception("Cannot join, the game has started")

      self.enter_room(sid, room)
      self.set_username(sid, username)
      members = [self.get_username(member['socketid']) for member in GameService().join_game(sid, username, room)]
      self.emit("update_lobby", {"members" : members}, room=room)
      print(members)

    except Exception as e:
      print(f"ERROR: {e}")
      self.emit("error", {"message" : f"Error: {e}"}, room=sid)
      # TODO: use a logger??

  @app_context
  def on_leave_room(self, sid, data):
    try:
      room = [room for room in self.rooms(sid) if room != sid][0]
      GameService().leave_game(sid, room)
    except Exception as e: 
      print(f"ERROR: {e}")
      self.emit("error", {"message" : f"Error: {e}"}, room=sid)
    
  
  # TODO: only the game creator can start
  @app_context
  def on_start_game(self, sid):
    room = [room for room in self.rooms(sid) if room != sid][0]
    GameService().start_game(room)
    self.emit("start_game", {"seed" : randrange(999)}, room=room)
  
  @app_context
  def on_register_vote(self, sid, data):
    movie_id = data["movie_id"]
    room = [room for room in self.rooms(sid) if room != sid][0]
    if GameService().game_vote(sid, room, movie_id):
      self.emit("pick_movie", {"movie_id" : movie_id}, room=room)
  
  def enter_room(self, sid, room, namespace=None):
    return self.server.enter_room(sid, room, namespace=namespace or self.namespace)
  
  def leave_room(self, sid, room, namespace=None):
    return self.server.leave_room(sid, room, namespace=namespace or self.namespace)

  def get_username(self, sid):
    with self.session(sid) as session:
      username = session["username"]
    return username
  
  def set_username(self, sid, username):
    with self.session(sid) as session:
      session["username"] = username
