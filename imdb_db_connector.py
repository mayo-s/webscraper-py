import mysql.connector
from mysql.connector import Error
import datetime
import json

# Connect to local database
def db_connect():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="imdb"
        )
        if db.is_connected():
            print('Connected to IMDb database')
            return db;
    except Error as e:
        print (e)

def db_close():
    db.close()
    print ('Connection closed')

# INSERT new movie dataset
def insert_movie(title, imdb_id, url, image_url, release_date):
    sql = "INSERT INTO movies (title, imdb_id, url, image_url, release_date) VALUES (%s, %s, %s, %s, %s)"
    val = (title, imdb_id, url, image_url, release_date)
    try:
        dbc = db.cursor()
        dbc.execute(sql, val)
        db.commit()
    except Error as e:
        print(e)

# Read JSON file
def json_read(filename):
    with open(filename) as movies:
        data = json.load(movies)
    return data

# INSERT all movies from JSON file
def insert_all_movies():
    print ('INSERT in progress... ')
    upcoming_movies = json_read('imdb_data.json')
    for movie in upcoming_movies:
        title = movie.get('title')
        imdb_id = movie.get('imdb_id')
        url = movie.get('url')
        image_url = movie.get('poster_url')
        release_date = movie.get('release_date')
        insert_movie(title, imdb_id, url, image_url, release_date)
    print ('INSERT successful')

# JSON dump
def json_dump(data):
    print ("JSON dump in progress... ")
    movies = []
    for movie in data:
        release_date = movie[5].strftime("%d %B %Y")
        movies.append({
            'id':movie[0],
            'title':movie[1],
            'imdb_id':movie[2],
            'url':movie[3],
            'image_url': movie[4],
            'release_date':release_date,
            'ranking':movie[6]})
    with open('imdb_db_data.json', 'w') as outfile:
        json.dump(movies, outfile, indent=4)
    print ("JSON dump successful")

# SELECT all movies database
def select_all():
    try:
        dbc = db.cursor()
        dbc.execute("SELECT * FROM movies")
        print ("SELECT * FROM movies successful")
        movies = dbc.fetchall()
        return movies
    except Error as e:
        print(e)


# TESTING ENVIRONMENT - work flow 
# connect to db
db = db_connect()
# 2.1 read json file and add movies to db
# insert_all_movies()
# 2.2 select all from movies table and dump  into json file
movies = select_all()
json_dump(movies)
# 3. close db connection
db_close()

