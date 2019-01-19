import json
from flask import jsonify
from imdb_db_connector import get_genres

# read JSON file
def json_read(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
    return data

def parse_movies(data):
    movies = []

    for movie in data:
        genres = get_genres(movie[0])
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
    movies = json.dumps(movies)
    return jsonify(movies)

def parse_genres(data):
    genres = []
    for genre in data:
        genres.append(genre[0])
    genres = json.dumps(genres)
    return jsonify(genres)

def parse_actors(data):
    actors = []
    for actor in data:
        actors.append(actor[0])
    actors = json.dumps(actors)
    return jsonify(actors)