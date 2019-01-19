from flask import Flask, request
from flask_cors import CORS
from imdb_db_connector import get_movies, get_all_genres, get_all_actors
from imdb_json_helper import parse_movies, parse_genres, parse_actors

app = Flask(__name__)
CORS(app)

@app.route('/getMovies')
def movies():
    actor = request.args.get('actor')
    if actor == None:
        actor = ""
    genre = request.args.get('genre')
    if genre == None:
        genre = ""
    rating = request.args.get('rating')
    if rating == None or rating == '':
        rating = 0

    movies = get_movies(actor, genre, rating)
    return parse_movies(movies)

@app.route('/getAllGenres')
def genres():
    genres = get_all_genres()
    return parse_genres(genres)

@app.route('/getAllActors')
def actors():
    actors = get_all_actors()
    return parse_actors(actors)

app.run(debug=True)
