from imdb_db_connector import db_connect, db_close, insert_all_movies
from imdb_json_helper import json_read
import os

# start scraper script
os.system("imdb_scraper.py")
# TODO get filename as return value
json_file = 'imdb_data.json'

# connect to database
db = db_connect()
# read json file
json_data = json_read(json_file)
# insert data from file to database
insert_all_movies(json_data)
# close database connection
db_close(db)