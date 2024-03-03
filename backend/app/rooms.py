import socketio
from sqids import Sqids

class RoomKeyTracker():
  keys = set()
  sqids = Sqids(min_length=4)

  def new_key(self) -> str:
    if self.keys:
      new_key = max(self.keys) + 1
    else:
      new_key = 0

    self.keys.add(new_key)
    return self.sqids.encode([new_key])

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

  def lock(self) -> None: 
    self.locked = True

  def unlock(self) -> None: 
    self.locked = False

  def get(self) -> set: 
    return self.members

  def is_empty(self) -> bool: 
    return len(self.members) <= 0

  def count(self) -> int: 
    return len(self.members)

  def submit_vote(self, title: str, vote: bool) -> None: 
    if self.locked: 
      if title in self.votes.keys():
        self.votes[title] += int(vote)
      else: 
        self.votes[title] = int(vote)
    else:
      raise Exception("Error: This game has not started yet...")

  def consensus_reached(self, title: str) -> bool: 
    return self.votes[title] >= self.count()

class RoomTracker():
  rooms = {}

  def create(self) -> str:
    room_key = RoomKeyTracker().new_key()
    self.rooms[room_key] = Room(room_key)
    return room_key

  def enter(self, sid: str, room_key: str) -> set:
    self.rooms[room_key].add_member(sid)
    return self.rooms[room_key].get()
  
  def leave(self, sid: str, room_key: str) -> set:
    self.rooms[room_key].remove_member(sid)
    return self.rooms[room_key].get()
  
  def start(self, room_key: str) -> None:
    self.rooms[room_key].lock()

  def vote(self, sid: str, room_key: str, title: str, vote: bool) -> bool:
    assert sid in self.rooms[room_key].members # TODO: do better...
    self.rooms[room_key].submit_vote(title, vote)
    ret = self.rooms[room_key].consensus_reached(title)
    return ret

  def exists(self, room: str) -> bool:
    return room in self.rooms.keys()






