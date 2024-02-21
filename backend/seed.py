#!/usr/bin/env python3
import sqlite3 
import sys

# function to scrape american movies from wikipedia using pandas
def create_movie_list(filename: str, start_year: int, end_year: int) -> None:
  import pandas as pd
  from tqdm import trange
  file = open(filename, "a")
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
        file.write(f"{row['Title']} *** {year}\n")

  file.close()

# seed our database using text file created from create_movie_list function
def seed_database(filename: str, db_name: str = "movies.db") -> None:
  con = sqlite3.connect(db_name) 
  cursor = con.cursor()
  data = []
  with open(filename, encoding='utf-8') as file:
    for line in file:
      title, year = line.split(" *** ")
      data.append((title, year)) 
      #print(f"title: {title}, year: {year}")

  cursor.executemany("INSERT INTO movies (title, year) VALUES (?, ?)", data)
  con.commit()
  

if __name__ == "__main__":
  # seed the database (by scraping wikipedia)
  # this is a bit overkill i think
  try:
    filename, start, end = sys.argv[1:4]
    create_movie_list(filename, int(start), int(end))
    seed_database(filename)
  except:
    print(f"Usage: ./{sys.argv[0]} <filename> <start_year> <end_year>")
