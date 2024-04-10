import socketio
from flask import Flask, g, request
from .routes import routes 
from .events import Namespace

flask_app = Flask(__name__)
flask_app.register_blueprint(routes)

from . import db_utils
#db_utils.init_app(flask_app)
@flask_app.teardown_appcontext
def teardown_db(exception):
  db_utils.close_db()

sio = socketio.Server(cors_allowed_origins="*")
sio.register_namespace(Namespace(flask_app, namespace="/test"))
#sio.register_namespace(TestNamespace(namespace="/test"))
app = socketio.WSGIApp(sio, flask_app)


"""
Note to self:

React in dev mode (strict mode) renders components twice, 

this is why socket endpoints are being called twice
"""