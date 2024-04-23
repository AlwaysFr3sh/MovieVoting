/*CREATE TABLE IF NOT EXISTS movies (
  --id INTEGER PRIMARY KEY AUTOINCREMENT,
  id integer PRIMARY KEY, -- imdb id, not storing the tt, hopefully that fine
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  genre TEXT,
  imdbrating DECIMAL
);*/

CREATE TABLE IF NOT EXISTS movies (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  genre TEXT,
  imdbRating DECIMAL,
  metascore INTEGER,
  rated TEXT,
  runtime INTEGER
);

-- TODO: add a random_seed integer column to this table
CREATE TABLE IF NOT EXISTS games (
  game_pin INTEGER PRIMARY KEY AUTOINCREMENT,
  status INTEGER NOT NULL,
  seed INTEGER
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
