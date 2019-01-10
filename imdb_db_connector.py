import mysql.connector
from mysql.connector import Error
import datetime
import json

# Connect to local database
def db_connect():
    try:
        db = mysql.connector.connect(
            option_files = '.db_pref.cnf'
        )
        if db.is_connected():
            print('Connected to IMDb database')
            return db;
    except Error as e:
        print (e)

def db_close(db):
    db.close()
    print ('Connection closed')

# SELECT all movie ids
def get_all_movie_ids():
    ids = []
    try:
        dbc = db.cursor()
        dbc.execute('SELECT imdb_id FROM movies')
        ids = dbc.fetchall()
        return ids;
    except Error as e:
        print(e)

# SELECT movie id by imdb_id
def get_movie_id(imdb_id):
    try:
        dbc = db.cursor()
        dbc.execute('SELECT id FROM movies WHERE imdb_id = \'' + imdb_id + '\'')
        movie_id = dbc.fetchall()
        if movie_id != []:
            movie_id = movie_id[0][0]
        return movie_id;
    except Error as e:
        print(e)

# SELECT genre id by genre name
def get_genre_id(genre):
    try:
        dbc = db.cursor()
        dbc.execute('SELECT id FROM genres WHERE genre = \'' + genre + '\'')
        genre_id = dbc.fetchall()
        if genre_id != []:
            genre_id = genre_id[0][0]
        return genre_id;
    except Error as e:
        print(e)

# SELECT actor id by imdb_id
def get_actor_id(imdb_id):
    try:
        dbc = db.cursor()
        dbc.execute('SELECT id FROM actors WHERE imdb_id = \'' + imdb_id + '\'')
        actor_id = dbc.fetchall()
        if actor_id != []:
            actor_id = actor_id[0][0]
        return actor_id;
    except Error as e:
        print(e)

# INSERT new movie dataset
def insert_movie(title, imdb_id, url, image_url, release_date, rating):
    sql = "INSERT INTO movies (title, imdb_id, url, image_url, release_date, rating) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (title, imdb_id, url, image_url, release_date, rating)
    try:
        dbc = db.cursor()
        dbc.execute(sql, val)
        movie_id = dbc.lastrowid
        db.commit()
        return movie_id
    except Error as e:
        print(e)

# INSERT new genre
def insert_genre(genre):
    sql = "INSERT INTO genres (genre) VALUES (%s)"
    val = (genre,)
    try:
        dbc = db.cursor()
        dbc.execute(sql, val)
        genre_id = dbc.lastrowid
        db.commit()
        return genre_id
    except Error as e:
        print(e)

# INSERT new actor dataset
def insert_actor(name, imdb_id):
    sql = "INSERT INTO actors (imdb_id, name) VALUES (%s, %s)"
    val = (imdb_id, name)
    try:
        dbc = db.cursor()
        dbc.execute(sql, val)
        actor_id = dbc.lastrowid
        db.commit()
        return actor_id
    except Error as e:
        print(e)

# INSERT new movie genre
def insert_movie_genre(movie_id, genre_id):
    sql = "INSERT INTO movieGenres (id_genre, id_movie) VALUES (%s, %s)"
    val = (genre_id, movie_id)
    try:
        dbc = db.cursor()
        dbc.execute(sql, val)
        db.commit()
    except Error as e:
        print(e)

# INSERT new movie actor
def insert_movie_actor(movie_id, actor_id):
    sql = "INSERT INTO movieActors (id_actor, id_movie) VALUES (%s, %s)"
    val = (actor_id, movie_id)
    try:
        dbc = db.cursor()
        dbc.execute(sql, val)
        db.commit()
    except Error as e:
        print(e)

# Read JSON file
def json_read(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
    return data


# INSERT all movies from JSON file
def insert_all_movies():
    print("Adding new movies...")
    upcoming_movies = json_read('imdb_data.json')
    db_movie_ids = get_all_movie_ids();

    for movie in upcoming_movies:
        movie_id = get_movie_id(movie.get('imdb_id'))
        if movie_id == []:
            title = movie.get('title')
            imdb_id = movie.get('imdb_id')
            url = movie.get('url')
            image_url = movie.get('poster_url')
            release_date = movie.get('release_date')
            rating = movie.get('rating')
            movie_id = insert_movie(title, imdb_id, url, image_url, release_date, rating)

            for genre in movie.get('genres'):
                genre_id = get_genre_id(genre)
                if genre_id == []:
                    genre_id = insert_genre(genre)

                insert_movie_genre(movie_id, genre_id)

            for actor in movie.get('actor_list'):
                actor_name = actor.get('name')
                actor_id = actor.get('id');
                actor_db_id = get_actor_id(actor_id)
                if actor_db_id == []:
                    actor_id = insert_actor(actor_name, actor_id)

                insert_movie_actor(movie_id, actor_id)

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

# TESTING ENVIRONMENT - work flow
# BEGIN
db = db_connect()
# 1 read json file and add movies to db
insert_all_movies()
# 2 close db connection
db_close(db)
