import mysql.connector
from mysql.connector import Error
import datetime

# connect to database
def db_connect():
  try:
    db = mysql.connector.connect(option_files = '.db_pref.cnf')
    if db.is_connected():
      print('Connected to IMDb database')
      return db;
  except Error as e:
    print (e)
       
# close database connection
def db_close(db):
  db.close()
  print ('Connection closed')

# SELECT movies from database
def get_movies(db, actor, genre, rating):
  actor = "%" + actor + "%"
  genre = "%" + genre + "%"

  if rating != 0:
    query = "SELECT DISTINCT j.* FROM (SELECT f.* FROM (SELECT m.* FROM movies m JOIN movieActors ma ON ma.id_movie = m.id JOIN actors a ON a.id = ma.id_actor AND a.name LIKE %s) as f JOIN movieGenres mg ON mg.id_movie = f.id JOIN genres g ON g.id = mg.id_genre AND g.genre LIKE %s) as j WHERE rating >= %s ORDER BY rating ASC"
    values = (actor, genre, rating)
  else:
    query = "SELECT DISTINCT j.* FROM (SELECT f.* FROM (SELECT m.* FROM movies m JOIN movieActors ma ON ma.id_movie = m.id JOIN actors a ON a.id = ma.id_actor AND a.name LIKE %s) as f JOIN movieGenres mg ON mg.id_movie = f.id JOIN genres g ON g.id = mg.id_genre AND g.genre LIKE %s) as j WHERE rating >= %s OR rating IS NULL ORDER BY release_date ASC"
    values = (actor, genre, rating)

  movies = []
  try:
    dbc = db.cursor()
    dbc.execute(query, values)
    movies = dbc.fetchall()
  except Error as e:
    print(e)

  return movies

# SELECT all genres from database
def get_all_genres(db):
  try:
    dbc = db.cursor()
    dbc.execute("SELECT genre FROM genres ORDER BY genre ASC")
    genres = dbc.fetchall()
  except Error as e:
    print(e)

  return genres

# SELECT genres for movie
def get_genres(db, movie_id): 
  try:
    dbc = db.cursor()
    dbc.execute("SELECT genres.genre FROM movieGenres INNER JOIN genres ON movieGenres.id_genre = genres.id WHERE movieGenres.id_movie = %s", (movie_id,))
    genres = dbc.fetchall()
  except Error as e:
    print(e)

  return genres;  

# SELECT all actors from database
def get_all_actors(db):
  try:
    dbc = db.cursor()
    dbc.execute("SELECT name FROM actors ORDER BY name ASC")
    actors = dbc.fetchall()
  except Error as e:
    print(e)

  return actors

# SELECT all movie ids
def get_all_movie_ids(db):
  ids = []
  try:
    dbc = db.cursor()
    dbc.execute('SELECT imdb_id FROM movies')
    ids = dbc.fetchall()
    return ids;
  except Error as e:
      print(e)

# SELECT movie id by imdb_id
def get_movie_id(db, imdb_id):
  try:
    dbc = db.cursor()
    dbc.execute('SELECT id FROM movies WHERE imdb_id = \'' + imdb_id + '\'')
    movie_id = dbc.fetchall()
    if movie_id != []:
      movie_id = movie_id[0][0]
    return movie_id;
  except Error as e:
    print(e)

# SELECT genre id by genre name
def get_genre_id(db, genre):
  try:
    dbc = db.cursor()
    dbc.execute('SELECT id FROM genres WHERE genre = \'' + genre + '\'')
    genre_id = dbc.fetchall()
    if genre_id != []:
      genre_id = genre_id[0][0]
    return genre_id;
  except Error as e:
    print(e)

# SELECT actor id by imdb_id
def get_actor_id(db, imdb_id):
  try:
    dbc = db.cursor()
    dbc.execute('SELECT id FROM actors WHERE imdb_id = \'' + imdb_id + '\'')
    actor_id = dbc.fetchall()
    if actor_id != []:
      actor_id = actor_id[0][0]
    return actor_id;
  except Error as e:
    print(e)

# INSERT new movie dataset
def insert_movie(db, title, imdb_id, url, image_url, release_date, rating):
  sql = "INSERT INTO movies (title, imdb_id, url, image_url, release_date, rating) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (title, imdb_id, url, image_url, release_date, rating)
  try:
    dbc = db.cursor()
    dbc.execute(sql, val)
    movie_id = dbc.lastrowid
    db.commit()
    return movie_id
  except Error as e:
    print(e)

# INSERT new genre
def insert_genre(db, genre):
  sql = "INSERT INTO genres (genre) VALUES (%s)"
  val = (genre,)
  try:
    dbc = db.cursor()
    dbc.execute(sql, val)
    genre_id = dbc.lastrowid
    db.commit()
    return genre_id
  except Error as e:
    print(e)

# INSERT new actor dataset
def insert_actor(db, name, imdb_id):
  sql = "INSERT INTO actors (imdb_id, name) VALUES (%s, %s)"
  val = (imdb_id, name)
  try:
    dbc = db.cursor()
    dbc.execute(sql, val)
    actor_id = dbc.lastrowid
    db.commit()
    return actor_id
  except Error as e:
    print(e)

# INSERT new movie genre
def insert_movie_genre(db, movie_id, genre_id):
  sql = "INSERT INTO movieGenres (id_genre, id_movie) VALUES (%s, %s)"
  val = (genre_id, movie_id)
  try:
    dbc = db.cursor()
    dbc.execute(sql, val)
    db.commit()
  except Error as e:
    print(e)

# INSERT new movie actor
def insert_movie_actor(db, movie_id, actor_id):
  sql = "INSERT INTO movieActors (id_actor, id_movie) VALUES (%s, %s)"
  val = (actor_id, movie_id)
  try:
    dbc = db.cursor()
    dbc.execute(sql, val)
    db.commit()
  except Error as e:
    print(e)

# INSERT all movies from JSON file
def insert_all_movies(db, json_data):
  print("Adding new movies...")
  upcoming_movies = json_data
  db_movie_ids = get_all_movie_ids(db);

  for movie in upcoming_movies:
    movie_id = get_movie_id(db, movie.get('imdb_id'))
    if movie_id == []:
      title = movie.get('title')
      imdb_id = movie.get('imdb_id')
      url = movie.get('url')
      image_url = movie.get('poster_url')
      release_date = movie.get('release_date')
      rating = movie.get('rating')
      movie_id = insert_movie(db, title, imdb_id, url, image_url, release_date, rating)

      for genre in movie.get('genres'):
        genre_id = get_genre_id(db, genre)
        if genre_id == []:
          genre_id = insert_genre(db, genre)

        insert_movie_genre(db, movie_id, genre_id)

      for actor in movie.get('actor_list'):
        actor_name = actor.get('name')
        actor_id = actor.get('id')
        actor_db_id = get_actor_id(db, actor_id)
        if actor_db_id == []:
          actor_id = insert_actor(db, actor_name, actor_id)

        insert_movie_actor(db, movie_id, actor_id)
