import mysql.connector
import datetime
import json

# connect to local db
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="imdb"
    )   
dbc = db.cursor(named_tuple=True)

# INSERT new movie dataset
def insert_movie(title, imdb_id, url, release_date):
    sql = "INSERT INTO movies (title,imdb_id, url, release_date) VALUES (%s, %s, %s, %s)"
    val = (title, imdb_id, url, release_date)
    try:
        dbc.execute(sql, val)
        db.commit()
    except mysql.connector.errors.OperationalError:
        print("Error: INSERT movie")

# Read JSON file
def json_read(filename):
    with open(filename) as movies:
        data = json.load(movies)
    return data

# INSERT all movies from scraped JSON file
def insert_all_movies():
    upcoming_movies = json_read('imdb_data.json')
    for movie in upcoming_movies:
        title = movie.get('title')
        imdb_id = movie.get('imdb_id')
        url = movie.get('url')
        # release_date.get('release_date')
        release_date = datetime.datetime(2037,3,1) # dummy date
        insert_movie(title, imdb_id, url, release_date)
    print ("INSERT successful")

# JSON dump
def json_dump(data):
    movies = []
    for movie in data:
        movies.append({'id':movie.id, 'title':movie.title, 'imdb_id':movie.imdb_id, 'url':movie.url, 'release_date':movie.release_date, 'ranking':movie.ranking})
    with open('imdb_db_data.json', 'w') as outfile:
        json.dump(movies, outfile, indent=4)
    print ("JSON dump successful")

# SELECT all movies database
def select_all():
    try:
        data = dbc.execute("SELECT * FROM movies")
        print ("SELECT * FROM movies successful")
        print ("JSON dump in progress... ")
        json_dump(data)
        print ("JSON dump completed")
    except mysql.connector.errors.OperationalError:
        print("Error: SELECT * ")

# insert_all_movies()
select_all()

db.close()

