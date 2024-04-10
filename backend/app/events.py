from random import randrange 

import socketio
from flask import current_app

from .rooms import RoomTracker
from .games import GameService

class Namespace(socketio.Namespace):

  def __init__(self, app, namespace=None):
    super().__init__(namespace=namespace)
    self.app = app
  
  def appcontext(foo):
    def magic(self, *args, **kwargs):
      with self.app.app_context():
        return foo(self, *args, **kwargs)
    return magic

  def on_connect(self, sid, environ):
    print(f"connected: {sid}")

  @appcontext
  def on_disconnect(self, sid):
    rooms_to_leave = [room for room in self.rooms(sid) if room != sid]
    for room in rooms_to_leave:
      room_members = [self.get_username(member['socketid']) for member in GameService().leave_game(sid, room)] 
      self.leave_room(sid, room)
      self.emit('update_lobby', {"members" : room_members}, room=room, skip_sid=sid)
    print(f"Disconnected: {sid}")
  
  @appcontext
  def on_join_room(self, sid, data):
    #with self.app.app_context():
    username, room = data["username"], data["room_key"]
    try:
      game = GameService().get_game(room)
      print(game)
      if game['status'] != 0:
        raise Exception("AHHHH")

      self.enter_room(sid, room)
      self.set_username(sid, username)
      members = [self.get_username(member['socketid']) for member in GameService().join_game(sid, username, room)]
      self.emit("update_lobby", {"members" : members}, room=room)
      print(members)

    except Exception as e:
      print(f"ERROR: {e}")
      #self.emit("exception", "Room does not exist", room=sid)
      # TODO: emit something when the room does not exist so that the client knows
      # TODO: use a logger??
  
  # TODO: only the game creator can start
  @appcontext
  def on_start_game(self, sid):
    room = [room for room in self.rooms(sid) if room != sid][0]
    GameService().start_game(room)
    self.emit("start_game", {"seed" : randrange(999)}, room=room)
  
  @appcontext
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