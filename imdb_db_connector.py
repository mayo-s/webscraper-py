import mysql.connector
from mysql.connector import Error
import datetime
import json
from flask import Flask
from flask import jsonify

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

# INSERT new movie dataset
def insert_movie(title, imdb_id, url, image_url, release_date):
    sql = "INSERT INTO movies (title, imdb_id, url, image_url, release_date) VALUES (%s, %s, %s, %s, %s)"
    val = (title, imdb_id, url, image_url, release_date)
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute(sql, val)
        movie_id = dbc.lastrowid
        db.commit()
        return movie_id
    except Error as e:
        print(e)

def insert_genre(genre):
    sql = "INSERT INTO genres (genre) VALUES (%s)"
    val = (genre,)
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute(sql, val)
        genre_id = dbc.lastrowid
        db.commit()
        return genre_id
    except Error as e:
        print(e)

def insert_movie_genre(movie_id, genre_id):
    sql = "INSERT INTO movieGenres (id_genre, id_movie) VALUES (%s, %s)"
    val = (genre_id, movie_id)
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute(sql, val)
        db.commit()
    except Error as e:
        print(e)

def insert_movie_actor(movie_id, genre_id):
    sql = "INSERT INTO movieActors (id_actor, id_movie) VALUES (%s, %s)"
    val = (actor_id, movie_id)
    try:
        db = db_connect()
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

def get_all_movie_ids():
    ids = []
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute('SELECT imdb_id FROM movies')
        ids = dbc.fetchall()
        db_close(db)
        return ids;
    except Error as e:
        print(e)

def get_genre_id(genre):
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute('SELECT id FROM genres WHERE genre = \'' + genre + '\'')
        genre_id = dbc.fetchall()
        if genre_id != []:
            genre_id = genre_id[0][0]
        db_close(db)
        return genre_id;
    except Error as e:
        print(e)

def get_movie_id(imdb_id):
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute('SELECT id FROM movies WHERE imdb_id = \'' + imdb_id + '\'')
        movie_id = dbc.fetchall()
        if movie_id != []:
            movie_id = movie_id[0][0]
            print(movie_id)
        db_close(db)
        return movie_id;
    except Error as e:
        print(e)

# INSERT all movies from JSON file
def insert_all_movies():
    print ('INSERT in progress... ')
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
            movie_id = insert_movie(title, imdb_id, url, image_url, release_date)

            for genre in movie.get('genres'):
                genre_id = get_genre_id(genre)
                print(genre_id)
                if genre_id == []:
                    print('INSERTING genre..')
                    genre_id = insert_genre(genre)

                insert_movie_genre(movie_id, genre_id)

            #for actor in movie.get('actor_list'):
                #actor_id = get_actor_id();


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

def parse_json(data):
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
            'ranking':movie[6] })
    return json.dumps(movies)


# SELECT all movies from database
def get_all_movies():
    db = db_connect()
    try:
        dbc = db.cursor()
        dbc.execute("SELECT * FROM movies")
        print ("SELECT * FROM movies successful")
        movies = dbc.fetchall()
    except Error as e:
        print(e)

    movies = parse_json(movies)
    return jsonify(movies)

def filter_movies(start, end, actor, genre, rating):
    db = db_connect()
    try:
        dbc = db.cursor()
        query = "SELECT * FROM movies WHERE (release_date BETWEEN %s AND %s)"
        values = (start, end)
        dbc.execute(query, values)

        movies = dbc.fetchall()
    except Error as e:
        print(e)

    movies = parse_json(movies)
    return jsonify(movies)




# TESTING ENVIRONMENT - work flow

# connect to db
# db = db_connect()
# 2.1 read json file and add movies to db
insert_all_movies()
# 2.2 select all from movies table and dump  into json file
# movies = select_all()
# json_dump(movies)
# 3. close db connection
# db_close()
