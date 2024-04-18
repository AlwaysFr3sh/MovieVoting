CREATE TABLE IF NOT EXISTS movies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  genre TEXT,
  imdbrating DECIMAL
);

-- TODO: add a random_seed integer column to this table
CREATE TABLE IF NOT EXISTS games (
  game_pin INTEGER PRIMARY KEY AUTOINCREMENT,
  status INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  socketid TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  game_pin INTEGER NOT NULL,
  FOREIGN KEY (game_pin) REFERENCES games (game_pin)
);

CREATE TABLE IF NOT EXISTS votes (
  movie_id INTEGER,
  count INTEGER NOT NULL,
  game_pin INTEGER NOT NULL,
  FOREIGN KEY (movie_id) REFERENCES movies (id),
  FOREIGN KEY (game_pin) REFERENCES games (game_pin),
  PRIMARY KEY (movie_id, game_pin)
);
