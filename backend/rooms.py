import socketio

# Method naming could be better?
# This class is bad, plz fix (all of them are kinda bad lol, i am a bad ooper)
# TODO: change to sets?
class RoomKeyTracker():
  keys = [0] 
  available_rooms = []
  
  def new_key(self) -> str:
    new_key = max(self.keys) + 1 if not self.available_rooms else self.available_rooms.pop()
    self.keys.append(new_key)
    return str(new_key)
  
  def recycle_key(self, room_key: str) -> None:
    room_key = int(room_key)
    self.keys.remove(room_key)
    self.available_rooms.append(room_key)


# TODO: Room should return something for add and remove to let us know if the operation was successful maybe???
class Room():
  def __init__(self, key: str):
    self.key = key
    self.members = set() 
    self.locked = False
    self.votes = {}

  def add_member(self, sid: str) -> None:
    if not self.locked:
      self.members.add(sid)

  def remove_member(self, sid: str) -> None:
    if not self.locked:
      self.members.remove(sid) 

  def lock(self) -> None: self.locked = True
  def unlock(self) -> None: self.locked = False
  def get(self) -> set: return self.members
  def is_empty(self) -> bool: return len(self.members) <= 0
  def count(self) -> int: return len(self.members)

  # this is ugly, very ugly, I want this to be one liner
  def submit_vote(self, title: str, vote: bool) -> None: 
    #self.votes[title] += vote if title in self.votes else self.votes[title] = int(vote)
    if self.locked: 
      if title in self.votes.keys():
        self.votes[title] += int(vote)
      else: 
        self.votes[title] = int(vote)
    else:
      raise Exception("Error: This game has not started yet...")

  def consensus_reached(self, title: str) -> bool: return self.votes[title] >= self.count()

# TODO : RoomTracker is currently coupled to sio object, should it be?
class RoomTracker():
  def __init__(self, sio: socketio.Server):
    self.rooms = {}
    self.sio = sio # is this bad???

  def create_room(self) -> str:
    room_key = RoomKeyTracker().new_key()
    self.rooms[room_key] = Room(room_key)
    return room_key

  # Currently assumes the room exists
  def enter(self, sid: str, room_key: str) -> set:
    self.rooms[room_key].add_member(sid)
    self.sio.enter_room(sid, room_key)
    return self.rooms[room_key].get()
  
  def leave(self, sid: str, room_key: str) -> set:
    self.rooms[room_key].remove_member(sid)
    self.sio.leave_room(sid, room_key)
    if self.rooms[room_key].is_empty():
      RoomKeyTracker().recycle_key(room_key)
      return self.rooms.pop(room_key).get()
    return self.rooms[room_key].get()
  
  def start_game(self, room_key: str) -> None:
    self.rooms[room_key].lock()

  def submit_vote(self, sid: str, room_key: str, title: str, vote: bool) -> bool:
    assert sid in self.rooms[room_key].members # TODO: do better...
    self.rooms[room_key].submit_vote(title, vote)
    ret = self.rooms[room_key].consensus_reached(title)
    return ret
