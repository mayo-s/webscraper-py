from flask import Flask, request
from flask_cors import CORS
from imdb_db_connector import get_movies, get_all_genres, get_all_actors, db_connect, db_close
from imdb_json_helper import parse_movies, parse_genres, parse_actors

app = Flask(__name__)
CORS(app)

@app.route('/getMovies')
def movies():
    db = db_connect()
    actor = request.args.get('actor')
    if actor == None:
        actor = ""
    genre = request.args.get('genre')
    if genre == None:
        genre = ""
    rating = request.args.get('rating')
    if rating == None or rating == '':
        rating = 0

    movies = get_movies(db, actor, genre, rating)
    result = parse_movies(db, movies)
    db_close(db)
    return result

@app.route('/getAllGenres')
def genres():
    db = db_connect()
    genres = get_all_genres(db)
    db_close(db)
    return parse_genres(genres)

@app.route('/getAllActors')
def actors():
    db = db_connect()
    actors = get_all_actors(db) 
    db_close(db)
    return parse_actors(actors)

app.run(debug=True)
