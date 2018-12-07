from flask import Flask, request
from flask_cors import CORS
import json
import mysql.connector
from mysql.connector import Error
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
    end = request.args.get('end')

    return filter_movies(start, end)

app.run(debug=True)
