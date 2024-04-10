#from .db_utils import get_db
from sqids import Sqids
from .db_utils import get_db, query_db, upsert_db

class GameService():

  sqids = Sqids(min_length=4)

  def create_game(self) -> str:
    query = "INSERT INTO games (status) VALUES (?)"
    db = get_db()
    cursor = db.execute(query, (0,)) # 0 is default status of a game, TODO: add enum to this code for readability (will still just be int in db)
    game_pin = self.sqids.encode([cursor.lastrowid])
    cursor.close()
    db.commit()
    return game_pin

  def join_game(self, sid: str, username: str, game_pin: str) -> list:
    # Insert sid into db (with foreign key to game) 
    # return a set of the sids that belong to the game-pin we've been given
    game_pin = self.sqids.decode(game_pin)[0]
    upsert_db("INSERT INTO users (socketid, username, game_pin) VALUES (?, ?, ?)", (sid, username, game_pin))
    query = "SELECT (socketid) FROM users WHERE game_pin=(?)"
    members = query_db(query, (game_pin,))
    return members

  def leave_game(self, sid: str, game_pin: str) -> list:
    # delete sid from game 
    # return members from game
    game_pin = self.sqids.decode(game_pin)[0]
    upsert_db("DELETE FROM users WHERE socketid=(?)", (sid,))
    query = "SELECT (socketid) FROM users WHERE game_pin=(?)"
    members = query_db(query, (game_pin,))
    return members

  def start_game(self, game_pin: str) -> None:
    # change status of game to 1
    game_pin = self.sqids.decode(game_pin)[0]
    upsert_db("UPDATE games SET status=1 WHERE game_pin=(?)", (game_pin,))

  def game_vote(self, sid: str, game_pin: str, movie_id: str) -> bool:
    game_pin = self.sqids.decode(game_pin)[0]

    if len(query_db("SELECT * FROM votes WHERE movie_id=(?) AND game_pin=(?)", (movie_id, game_pin))) > 0:
      query = """
              UPDATE votes
              SET count = CASE WHEN (?) IN (SELECT socketid FROM users where game_pin = (?)) THEN count+1 ELSE count END
              WHERE movie_id=(?) AND game_pin=(?);
              """
      upsert_db(query, (sid, game_pin, movie_id, game_pin))

    else:
      # TODO: check if user belongs to game here too
      upsert_db("INSERT INTO votes (movie_id, game_pin, count) VALUES (?, ?, ?)", (movie_id, game_pin, 1))

    members = query_db("SELECT * FROM users WHERE game_pin=(?)", (game_pin,))
    count = query_db("SELECT count FROM votes WHERE game_pin=(?) AND movie_id=(?)", (game_pin, movie_id))[0]["count"]
    return count >= len(members)

  def get_game(self, game_pin: str) -> bool:
    query = "SELECT * FROM games WHERE game_pin=(?)"
    game_pin = self.sqids.decode(game_pin)[0]
    return query_db(query, (game_pin,))[0]


if __name__ == "__main__": 
  import sqlite3
  from db_utils import make_dicts

  db = sqlite3.connect("../movies.db")
  db.row_factory = make_dicts

  def query_db(query, args=(), one=False):
    cursor = db.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

  game_pin = 1
  movie_id = 1

  query = "UPDATE votes SET count = CASE WHEN (?) IN (SELECT socketid FROM users where game_pin = (?)) THEN count+1 ELSE count END WHERE movie_id=(?) AND game_pin=(?);"
  db.execute(query, (123, game_pin, movie_id, game_pin))
  db.commit()

  query = "SELECT * FROM users WHERE game_pin=(?)"
  members = query_db(query, (game_pin,))
  query = "SELECT count FROM votes WHERE game_pin=(?) AND movie_id=(?)"
  count = query_db(query, (game_pin, movie_id))[0]["count"]
  print(f"The number of members in the room is {len(members)} and the number who voted for {movie_id} is {count}") 
  print(count >= len(members))


  db.close()