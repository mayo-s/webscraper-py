from flask import Flask
import json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# JSON dump
def json_dump(data):
    print ("JSON dump in progress... ")
    movies = []
    for movie in data:
        release_date = movie[4].strftime("%d %B %Y")
        movies.append({'id':movie[0], 'title':movie[1], 'imdb_id':movie[2], 'url':movie[3], 'release_date':release_date, 'ranking':movie[5]})
    with open('imdb_db_data.json', 'w') as outfile:
        json.dump(movies, outfile, indent=4)
    print ("JSON dump successful")

@app.route('/getAllMovies')
def get_all_movies():
    try:
        dbc = db.cursor()
        dbc.execute("SELECT * FROM movies")
        print ("SELECT * FROM movies successful")
        movies = dbc.fetchall()
    except Error as e:
        print(e)
    return json_dump(movies)

app.run(debug=True)
