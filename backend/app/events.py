import socketio
from random import randrange 
from .rooms import RoomTracker

class Namespace(socketio.Namespace):
  def on_connect(self, sid, environ):
    print(f"connected: {sid}")

  def on_disconnect(self, sid):
    rooms_to_leave = [room for room in self.rooms(sid) if room != sid]
    for room in rooms_to_leave:
      room_members = [self.get_username(member_sid) for member_sid in RoomTracker().leave(sid, room)]
      self.leave_room(sid, room)
      self.emit("update_lobby", {"members" : room_members}, room=room, skip_sid=sid)
    print(f"Disconnected: {sid}")

  def on_join_room(self, sid, data):
    username, room_key = data["username"], data["room_key"]
    if RoomTracker().exists(room_key):
      with self.session(sid) as session:
        session["username"] = username
      sids = list(RoomTracker().enter(sid, room_key))
      self.enter_room(sid, room_key)
      room_members = [self.get_username(member_sid) for member_sid in sids]
      self.emit("update_lobby", {"members" : room_members}, room=room_key)
    else:
      self.emit("exception", "Error: Room does not exist", room=sid)

  def on_start_game(self, sid):
    room_key = [room for room in self.rooms(sid) if room != sid][0]
    RoomTracker().start(room_key)
    self.emit("start_game", {"seed" : randrange(999)}, room=room_key)

  def on_register_vote(self, sid, data):
    title, vote = data["title"], data["vote"]
    room_key = [room for room in self.rooms(sid) if room != sid][0]
    if RoomTracker().vote(sid, room_key, title, vote):
      self.emit("pick_movie", {"title" : title}, room=room_key)
  
  def enter_room(self, sid, room, namespace=None):
    return self.server.enter_room(sid, room, namespace=namespace or self.namespace)
  
  def leave_room(self, sid, room, namespace=None):
    return self.server.leave_room(sid, room, namespace=namespace or self.namespace)

  def get_username(self, sid):
    with self.session(sid) as session:
      username = session["username"]
    return username
