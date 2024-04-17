#!/usr/bin/env python3

import sys
import os
from argparse import ArgumentParser

import sqlite3 
import pandas as pd
from tqdm import tqdm, trange

# function to scrape american movies from wikipedia using pandas
def create_movie_list_from_wikipedia(filename: str, start_year: int, end_year: int) -> None:
  f = open(filename, "a")
  for year in range(start_year, end_year):
    print(f"Downloading {year}")
    try:
      df_list = pd.read_html(f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}")  
    except Exception as e:
      print(f"Failed to read html using pandas: \n{e}")
      continue
    # 2009 has weird table inside table so we need different range than other years, stupid 2009
    table_range = (3, 7) if year == 2010 else (2, 6)
    for i in trange(*table_range):
      for index, row in df_list[i].iterrows():
        f.write(f"{row['Title']} *** {year}\n")

  f.close()

# seed our database using text/csv file created from create_movie_list function
# TODO: naming for this func is pretty rough
def insert_into_database(filename: str, db_name: str) -> None:
  con = sqlite3.connect(db_name) 
  cursor = con.cursor()
  data = []
  print(f"Seeding database: {db_name} with data from from {filename}...")
  with open(filename, encoding='utf-8') as f:
    for line in tqdm(f):
      title, year = line.split(" *** ")
      data.append((title, year)) 

  cursor.executemany("INSERT INTO movies (title, year) VALUES (?, ?)", data)
  con.commit()
  

def seed_database():
  parser = ArgumentParser(
    prog="seed.py",
    description="Movie Decider sqlite3 database seeding tool",
  )
  # seed argument is so we can call this function from flask cli
  parser.add_argument("seed", nargs="?")
  parser.add_argument("-f", "--filename", required=False, default="AmericanMovies.txt")
  parser.add_argument("-d", "--dbname", required=False, default="movies.db")
  parser.add_argument("-s", "--start_year", required=False, choices=range(1970, 2024), default=1970)
  parser.add_argument("-e", "--end_year",  required=False, choices=range(1970, 2024), default=1970)
  args = parser.parse_args()
  #if not os.path.isfile(args.filename): create_movie_list_from_wikipedia(args.filename, args.start_year, args.end_year)
  #insert_into_database(args.filename, args.dbname)
  print("Done!")

if __name__ == "__main__":
  seed_database()
