# webscraper-py
### Playing around with webscraper technologies using Python3 and BeautifulSoup4.
 
Targeting imdb.com/calendar to scrape names, links and release dates of upcoming movies.  
Scraped data will be written to a json file in project folder.  
  
Here is an example of what the scraped data looks like  

![alt text](https://github.com/mayo-s/webscraper-py/blob/master/img/sample_print.png)
  
## Database
  
![alt text](https://github.com/mayo-s/webscraper-py/blob/master/img/imdb_scraper_db-model.png)
  
## Setup instructions
(using terminal - follow on your own risk ;-) )  
  
- (install python3 if not already done `> brew install python`)  
- move to your project folder `> cd "path/projectFolder"`  
- create virtual environment `> python3 -m venv "/projectFolder/"`  
- activate virtual environment `> source bin/activate`  
- (urllib and json libraries should already be included in your python3 installation)  
- install BeautifulSoup library `> pip install beautifulsoup4`  
- install Flask `> pip install flask`  
- add flask CORS `> pip install -U flask_cors`  

- run scraper script `> python3 imdb_scraper_action.py`  
  - dumps scraped data into json-file (imdb_data.json) 
  - inserts scraped data into database
- run flask `> python3 imdb_controller.py`  
  - check i.e. http://127.0.0.1:5000/getMovies (will return json-reponse)  
  - /getMovies  
  	- Available filter parameter: actor, genre, rating  
  	- e.g. http://127.0.0.1:5000/getMovies?genre="Adventure"&rating=7  

  - /getAllActors  
  - /getAllGenres  
  
- when done working - deactivate virtual environment > deactivate  
  
### Frontend
There is an corresponding Frontend available  
check it out at https://github.com/ViviZa/react-app  
