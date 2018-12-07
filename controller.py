from flask import Flask, request
from flask_cors import CORS
from imdb_db_connector import get_all_movies
from imdb_db_connector import filter_movies

app = Flask(__name__)
CORS(app)

@app.route('/getAllMovies')
def all_movies():
    return get_all_movies()

@app.route('/filter')
def filter():
    #request date format must be '2019-01-01'
    start = request.args.get('start')
    if start == None:
        start = '2000-01-01'

    end = request.args.get('end')
    if end == None:
        end = '3000-01-01'

    actor = request.args.get('actor')
    if actor == None:
        nothing

    genre = request.args.get('genre')
    if genre == None:
        nothing

    rating = request.args.get('rating')
    if rating == None:
        nothing

    return filter_movies(start, end, actor, genre, rating)

app.run(debug=True)
