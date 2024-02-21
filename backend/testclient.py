import sys
import socketio

sio = socketio.Client()

@sio.event
def connect():
  print('connected')

@sio.event
def disconnect():
  print('disconnected')

@sio.event
def user_joined(username):
  print(f"{username} has connected")

@sio.event
def user_left(username):
  print(f"{username} disconnected")

@sio.event
def print_something(something):
  print(something)

@sio.event
def start_game(seed):
  print(f"the game has started, please request your movie list using the seed {seed}")

@sio.event
def update_lobby(data):
  members = data["members"]
  print(f"members: {' '.join(members)}")

@sio.event
def pick_movie(data):
  title = data["title"]
  print(f"A consensus has been reached, we all have agreed to watch {title}")



def main(username: str):
  sio.connect('http://localhost:8000', headers={ 'X-Username' : username })
  #sio.connect("http://localhost:8000")

  #sio.emit("join_room", {"room_key" : "0", "username": username})

  #if username == "bob":
    #sio.emit("start_game", "0") # should we just try to calculate the room key on the server side rather than have the client know it? probably not

  #if username == "bob":
    #sio.emit("create_room", {"username" : username})
  import requests
  result = requests.get("http://localhost:8000/create_room")
  print(result.json()['room_key'])


  #sio.emit("join_room", {"username": username, "room_key": "1"})

  #sio.emit("register_vote", {"room_key" : "1", "title" : "Kung Fu Panda", "vote" : True})

  sio.wait()

if __name__ == '__main__':
  main(sys.argv[1] if len(sys.argv) > 1 else None)
