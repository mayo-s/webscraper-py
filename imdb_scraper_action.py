from imdb_scraper import scrape
from imdb_db_connector import db_connect, db_close, insert_all_movies
from imdb_json_helper import json_read

# start scraper script
json_file = scrape()
# connect to database
db = db_connect()
# read json file
json_data = json_read(json_file)
# insert data from file to database
insert_all_movies(db, json_data)
# close database connection
db_close(db)