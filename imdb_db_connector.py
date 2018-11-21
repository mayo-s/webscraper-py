import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="imdb"
    )   
dbc = db.cursor()

# INSERT new (complete) movie dataset
def insert_all(title, genres, url, release_date):
    sql = "INSERT INTO movies (title, genres, url, release_date) VALUES (%s, %s, %s, %s)"
    val = (title, "", url, release_date)
    try:
        dbc.execute(sql, val)
        db.commit()
        print ("INSERT successful")
    except mysql.errors.OperationalError:
        print("error")

title = "The Girl in the Spider's Web: A New Dragon Tattoo Story"
genres = ["Crime", "Drama", "Thriller"]
url =  "https://www.imdb.com/title/tt5177088/?ref_=rlm"
release_date =  "22 November 2018"

insert_all(title, genres, url, release_date)

db.close()

