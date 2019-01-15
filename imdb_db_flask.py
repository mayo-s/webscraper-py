from imdb_db_connector import db_connect, db_close
import json
from flask import jsonify

def parse_movies(data):
    movies = []
    db = db_connect()

    for movie in data:
        try:
            dbc = db.cursor()
            dbc.execute("SELECT genres.genre FROM movieGenres INNER JOIN genres ON movieGenres.id_genre = genres.id WHERE movieGenres.id_movie = %s", (movie[0],))
            genres = dbc.fetchall()
        except Error as e:
            print(e)

        release_date = movie[5].strftime("%d %B %Y")
        movies.append({
            'id':movie[0],
            'title':movie[1],
            'imdb_id':movie[2],
            'url':movie[3],
            'image_url': movie[4],
            'release_date':release_date,
            'rating':movie[6],
            'genres':genres})
    return json.dumps(movies)

def parse_genres(data):
    genres = []
    for genre in data:
        genres.append(genre[0])
    return json.dumps(genres)

def parse_actors(data):
    actors = []
    for actor in data:
        actors.append(actor[0])
    return json.dumps(actors)

# SELECT all movies from database
def get_all_movies():
    db = db_connect()
    try:
        dbc = db.cursor()
        dbc.execute("SELECT * FROM movies")
        movies = dbc.fetchall()
    except Error as e:
        print(e)

    movies = parse_movies(movies)
    return jsonify(movies)

def get_movies(actor, genre, rating):
    actor = "%" + actor + "%"
    genre = "%" + genre + "%"

    query = "SELECT DISTINCT j.* FROM (SELECT f.* FROM (SELECT m.* FROM movies m JOIN movieActors ma ON ma.id_movie = m.id JOIN actors a ON a.id = ma.id_actor AND a.name LIKE %s) as f JOIN movieGenres mg ON mg.id_movie = f.id JOIN genres g ON g.id = mg.id_genre AND g.genre LIKE %s) as j WHERE rating >= %s OR rating IS NULL ORDER BY rating ASC"
    values = (actor, genre, rating)

    movies = []
    db = db_connect()
    try:
        dbc = db.cursor()
        dbc.execute(query, values)
        movies = dbc.fetchall()
    except Error as e:
            print(e)

    movies = parse_movies(movies)
    return jsonify(movies)

# SELECT all genres from database
def get_all_genres():
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute("SELECT genre FROM genres")
        genres = dbc.fetchall()
    except Error as e:
        print(e)

    genres = parse_genres(genres)
    return jsonify(genres)

# SELECT all movies from database
def get_all_actors():
    try:
        db = db_connect()
        dbc = db.cursor()
        dbc.execute("SELECT name FROM actors")
        actors = dbc.fetchall()
    except Error as e:
        print(e)

    actors = parse_actors(actors)
    return jsonify(actors)
