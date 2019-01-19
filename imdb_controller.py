from flask import Flask, request
from flask_cors import CORS
from imdb_db_flask import get_movies, get_all_genres, get_all_actors

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

    return get_movies(actor, genre, rating)

@app.route('/getAllGenres')
def genres():
    return get_all_genres()

@app.route('/getAllActors')
def actors():
    return get_all_actors()

app.run(debug=True)
