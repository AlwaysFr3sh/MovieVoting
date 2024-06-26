import sys
#from random import randrange
import random

#from .db_utils import get_db
from sqids import Sqids
from .db_utils import get_db, query_db, upsert_db

# TODO: consider lifting db stuff out and separating from business logic with an ORM or something
class GameService():

  sqids = Sqids(min_length=4)

  def create_game(self) -> str:
    query = "INSERT INTO games (status, seed) VALUES (?, ?)"
    seed = random.randrange(999)
    db = get_db()
    cursor = db.execute(query, (0, seed)) # 0 is default status of a game, TODO: add enum to this code for readability (will still just be int in db)
    game_pin = self.sqids.encode([cursor.lastrowid])
    cursor.close()
    db.commit()
    return game_pin

  def join_game(self, sid: str, username: str, game_pin: str) -> list:
    # Insert sid into db (with foreign key to game) 
    # return a set of the sids that belong to the game-pin we've been given
    game_pin = self.sqids.decode(game_pin)[0]
    upsert_db("INSERT INTO users (socketid, username, game_pin) VALUES (?, ?, ?)", (sid, username, game_pin))
    members = query_db("SELECT (socketid) FROM users WHERE game_pin=(?)", (game_pin,))
    return members

  def leave_game(self, sid: str, game_pin: str) -> list:
    # delete sid from game 
    # return members from game
    game_pin = self.sqids.decode(game_pin)[0]
    upsert_db("DELETE FROM users WHERE socketid=(?)", (sid,))
    members = query_db("SELECT (socketid) FROM users WHERE game_pin=(?)", (game_pin,))
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
              SET count = CASE WHEN (?) IN (SELECT socketid FROM users WHERE game_pin = (?)) THEN count+1 ELSE count END
              WHERE movie_id=(?) AND game_pin=(?);
              """
      upsert_db(query, (sid, game_pin, movie_id, game_pin))

    else:
      # TODO: check if user belongs to game here too
      upsert_db("INSERT INTO votes (movie_id, game_pin, count) VALUES (?, ?, ?)", (movie_id, game_pin, 1))

    members = query_db("SELECT * FROM users WHERE game_pin=(?)", (game_pin,))
    count = query_db("SELECT count FROM votes WHERE game_pin=(?) AND movie_id=(?)", (game_pin, movie_id))[0]["count"]
    return count >= len(members)
  
  def get_movies(self, game_pin: str, limit: int=5, rows: str="*"):
    # TODO: should probably do verification with sid rather than username
    # TODO: error handling surrounding existence of a game? code currently assumes game exists
    # https://gist.github.com/eslof/88492e6a7c2eb90d61748227ab3b3fb1
    game_pin = self.sqids.decode(game_pin)[0]
    seed = query_db("SELECT seed from games WHERE game_pin=(?)", (game_pin,), one=True)["seed"]
    r = random.Random(seed)
    db = get_db()
    db.create_collation("seeded_random", lambda s1, s2 : r.randint(-1, 1)) #seeded_random_collation)
    #cursor = db.execute("SELECT * FROM movies ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT (?)", (limit,))
    # TODO: is the format string here secure?
    cursor = db.execute(f"SELECT {rows} FROM movies ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT (?)", (limit,))
    ret = cursor.fetchall()
    cursor.close()
    return ret

  def get_game(self, game_pin: str) -> bool:
    game_pin = self.sqids.decode(game_pin)[0]
    return query_db("SELECT * FROM games WHERE game_pin=(?)", (game_pin,))[0]

