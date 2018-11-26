import mysql.connector
import datetime
import json

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="imdb"
    )   
dbc = db.cursor()

# INSERT new movie dataset
def insert_movie(title, imdb_id, url, release_date):
    sql = "INSERT INTO movies (title,imdb_id, url, release_date) VALUES (%s, %s, %s, %s)"
    val = (title, imdb_id, url, release_date)
    try:
        dbc.execute(sql, val)
        db.commit()
        print ("INSERT successful")
    except mysql.connector.errors.OperationalError:
        print("Error: INSERT movie")

def json_read(filename):
    with open(filename) as movies:
        data = json.load(movies)
    return data

# INSERT all movies from scraped json file
def insert_movies():
    upcoming_movies = json_read('imdb_data.json')
    for movie in upcoming_movies:
        title = movie.get('title')
        imdb_id = movie.get('imdb_id')
        url = movie.get('url')
        # release_date.get('release_date')
        release_date = datetime.datetime(2037,3,1) # dummy date
        insert_movie(title, imdb_id, url, release_date)

insert_movies()

db.close()

