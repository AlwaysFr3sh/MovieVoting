#!/usr/bin/env python3

import sys
import os
import requests
from argparse import ArgumentParser
from typing import List

import sqlite3 
import pandas as pd
from tqdm import tqdm, trange

# temporary scuffed solution
def omdb_key():
  f = open("../secrets.txt", "r")
  ret = f.read().strip()
  f.close()
  return ret

def omdb(title: str, year: int, key: str): # TODO: type hint the return
  title = str(title).replace(" ", "+")
  r = requests.get(f"http://www.omdbapi.com/?apikey={key}&t={title}&y={year}")
  return r.json()

def scrape_wikipedia(start_year: int, end_year: int) -> List[tuple]:
  ret = []
  for year in range(start_year, end_year):
    print(f"downloading {year}...")
    try:
      df_list = pd.read_html(f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}")  
    except Exception as e:
      print(f"Failed to read html using pandas: \n{e}")
      continue
    # 2009 has weird table inside table so we need different range than other years, stupid 2009
    table_range = (3, 7) if year == 2010 else (2, 6)
    for i in trange(*table_range):
      for index, row in df_list[i].iterrows():
        ret.append((row["Title"], year))
  
  return ret

# seed our database using text/csv file created from create_movie_list function
# TODO: naming for this func is pretty rough
#def insert_into_database(filename: str, db_name: str) -> None:
def insert_into_database(movies: List[tuple], db_name: str) -> None:
  con = sqlite3.connect(db_name) 
  cursor = con.cursor()
  omdb_api_key = omdb_key()
  print(f"Seeding database: {db_name}...")
  for title, year in tqdm(movies):
    d = omdb(title, year, omdb_api_key)
    query = """
    INSERT INTO movies (id, title, year, genre, imdbRating, metascore, rated, runtime)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    if d["Response"].strip() == "True":
      args = (d["imdbID"].replace("tt", ""), 
      title, 
      year, 
      d["Genre"], 
      d["imdbRating"], 
      d["Metascore"], 
      d["Rated"], 
      d["Runtime"].replace(" min", ""))

      try:
        cursor.execute(query, args)
      except Exception as e:
        print(f"Error: {e} Movie: {title} - {year}")

  con.commit()
  con.close()
  

def seed_database():
  parser = ArgumentParser(
    prog="seed.py",
    description="Movie Decider sqlite3 database seeding tool",
  )
  # seed argument is so we can call this function from flask cli
  parser.add_argument("seed", nargs="?")
  parser.add_argument("-d", "--dbname", required=False, default="movies.db")
  parser.add_argument("-s", "--start_year", required=False, choices=range(1970, 2024), type=int)
  parser.add_argument("-e", "--end_year",  required=False, choices=range(1970, 2024), type=int)
  args = parser.parse_args()
  #if not os.path.isfile(args.filename): create_movie_list_from_wikipedia(args.filename, args.start_year, args.end_year)
  movies = scrape_wikipedia(args.start_year, args.end_year)
  insert_into_database(movies, args.dbname)
  print("Done!")

if __name__ == "__main__":
  seed_database()
