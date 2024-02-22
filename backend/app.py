# TODO: stuff to add / fix 

# [X] replace "print_something" event with proper event for disconnect and join_room 
# [X] handle room_key generation if no room key is provided
# [X] implement "locking" for RoomTracker
# [X] Implement register_vote (make a shitty implementation & we can use dependency injection later to swap out with something like redis if necessary )
# [X] "create_room" event should also emit the room key back to the client 

# [X] Check that sid is type string (otherwise ur type hints will make you look pretty dumb)
# [X] Verify that an sid casting a vote, belongs to the room they are voting for before submitting the vote
# [X] Should i implement something to prevent voting until the game has started serverside?

# [ ] Unit Tests

# [ ] Flask routes should be apart of a blueprint that we import into our main file
# [ ] See if we can do a similar blueprint thingy with the socketio routes too

import socketio
from random import randrange
from flask import Flask

pp = Flask(__name__)

sio = socketio.Server(cors_allowed_origins="http://localhost:3000")
app = socketio.WSGIApp(sio, pp)

# Custom rooms built on top of sio, I think this is necessary but maybe the docs just suck
from rooms import RoomTracker
room_tracker = RoomTracker(sio)

# -- Http Endpoints -- 
# TODO: rename flask app from 'pp' to something mature, sensible and descriptive
# TODO: what method should this be
# TODO: should this be http or socket event?
@pp.route('/create_room', methods=['POST'])
def create_room():
  room_key = room_tracker.create_room()
  return {"room_key" : room_key}

# -- Socket Events --
@sio.event
def connect(sid, environ):
  print(f"Connected: {sid}")

# TODO: maybe don't delete room immediately on disconnection, this breaks things 
#       if only one person is in the room, leaves then reconnects
@sio.event
def disconnect(sid):
  rooms_to_leave = [room for room in sio.rooms(sid) if room != sid]
  print(f"rooms to leave: {' '.join(rooms_to_leave)}") #Debug, remove when done
  for room in rooms_to_leave:
    room_members = [get_username(member_sid) for member_sid in room_tracker.leave(sid, room)]
    sio.emit("update_lobby", {"members" : room_members}, room=room, skip_sid=sid)

  print(f"Disconnected: {sid}")

@sio.event
def join_room(sid, data):
  username, room_key = data["username"], data["room_key"]
  with sio.session(sid) as session:
    session['username'] = username
  sids = list(room_tracker.enter(sid, room_key))
  room_members = [get_username(member_sid) for member_sid in sids]
  sio.emit("update_lobby", {"members" : room_members}, room=room_key)

@sio.event
def start_game(sid):
  room_key = [room for room in sio.rooms(sid) if room != sid][0] #TODO This is a hack, this whole fucking backend sucks ass
  room_tracker.start_game(room_key)
  sio.emit('start_game', {"seed" : randrange(10000)}, room=room_key)

@sio.event
def register_vote(sid, data):
  room_key, title, vote = data["room_key"], data["title"], data["vote"]
  if room_tracker.submit_vote(sid, room_key, title, vote):
    sio.emit("pick_movie", {"title" : title}, room=room_key)


# -- Logic --
def get_username(sid:str) -> str:
  with sio.session(sid) as session:
    username = session["username"]
  return username
