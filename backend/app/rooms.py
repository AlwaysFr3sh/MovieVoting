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


#------------------------------------------------
# Redis Replacement code because in-memory probably won't work because 
# gunicorn is gonna parallel this b*tch





if __name__ == "__main__":

  import sqlite3
  from db_utils import make_dicts

  db = sqlite3.connect("../movies.db")
  db.row_factory = make_dicts

  query = "INSERT INTO games (status) VALUES (?)"
  cursor = db.execute(query, (0,))
  my_id = cursor.lastrowid
  db.commit()
  db.close()

  print(f"Raw id: {my_id}, game-pin: {RoomKeyTracker.sqids.encode([my_id])}")
  """

  from mongoengine import EmbeddedDocument, Document, StringField, IntField, BooleanField, ListField, EmbeddedDocumentField

  class User(EmbeddedDocument):
    sid = StringField(required=True)
    username = StringField(required=True)
  
  class MovieVote(EmbeddedDocument):
    title = StringField(required=True)
    count = IntField(default=lambda: 0)

  class Game(Document):
    started = BooleanField(default=lambda: False)
    members = ListField(EmbeddedDocumentField(User), default=list)
    votes = ListField(EmbeddedDocumentField(MovieVote), default=list) 

  from mongoengine import connect, disconnect

  uri = "mongodb+srv://tomhollo123:2YIBkU3aFk4f80dD@cluster0.fzxqnt6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
  connect(host=uri)
  print("Woo Hoo! Connected")

  game = Game(
    members=[
        User(sid="12345", username="Tom"),
        User(sid="67890", username="Ashley")
      ], 
      votes=[
        MovieVote(title="Star Wars", count=2), 
        MovieVote(title="Kung Fu Panda", count=1)
      ]
    )
  game.save()
  
  print(game.to_json())


  disconnect()
  """