from flask import Blueprint 

# TODO: feels like a dodgy import?
from seed import seed_database 

commands = Blueprint('commands', __name__, cli_group=None) 

@commands.cli.command("seed")
def seed():
  seed_database()