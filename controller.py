from flask import Flask, request
from flask_cors import CORS
from imdb_db_connector import get_all_movies
from imdb_db_connector import get_all_genres
from imdb_db_connector import get_all_actors
from imdb_db_connector import filter_movies

app = Flask(__name__)
CORS(app)

@app.route('/getAllMovies')
def all_movies():
    actor = request.args.get('actor')
    genre = request.args.get('genre')
    rating = request.args.get('rating')

    return get_all_movies(actor, genre, rating)

@app.route('/getAllGenres')
def all_genres():
    return get_all_genres()

@app.route('/getAllActors')
def all_actors():
    return get_all_actors()

@app.route('/getSearch')
def filter():
    actor = request.args.get('actor')
    if actor == None:
        nothing

    genre = request.args.get('genre')
    if genre == None:
        nothing

    rating = request.args.get('rating')
    if rating == None:
        nothing

    return filter_movies(actor, genre, rating)

app.run(debug=True)
