import socketio
from flask import Flask, g, request
from app.routes import routes 
from app.events import Namespace

flask_app = Flask(__name__)
flask_app.register_blueprint(routes)
sio = socketio.Server(cors_allowed_origins="http://localhost:3000")
sio.register_namespace(Namespace("/test"))
app = socketio.WSGIApp(sio, flask_app)

# TODO: is this working??
@flask_app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

"""
SERVER:
-------------------------------------------------
[ ] Room keys:
store room key manager class in session object so 
we aren't screwed by multithreading nonsense

Do same thing with other room management object or put in Redis or something
-------------------------------------------------
[ ] Robust Reconnections
I have no idea how this will turn out
-------------------------------------------------
[ ] Username should be give on connection
-------------------------------------------------
[ ] Unit Tests for rooms.py
-------------------------------------------------
-------------------------------------------------
"""