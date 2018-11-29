# webscraper-py
Playing around with webscraper technologies using Python3 and BeautifulSoup4.
 
Targeting imdb.com/calendar to scrape names, links and release dates of upcoming movies.
Scraped data will be written to a json file in project folder.

Here is an example of what the scraped data looks like

![alt text](https://github.com/mayo-s/webscraper-py/blob/master/sample_print.png)

Sample Setup (using terminal - follow on your own risk ;-) )
- (install python3 if not already done > brew install python)
- move to your project folder > cd "path/projectFolder"
- create virtual environment > python3 -m venv "/projectFolder/"
- activate virtual environment > source "/projectFolder/bin/activate"
- (urllib and json libraries should already be included in your python3 installation)
- install BeautifulSoup library > sudo pip install beautifulsoup4
- install Flask > sudo pip install flask

- run scraper script > python3 imdb_scraper.py
  - will dump scraped data into json-file (imdb_data.json)
- run flask > python3 imdb_db_connector.py
  - check http://127.0.0.1:5000/getAllMovies (will return json-reponse)

- when done working - deactivate virtual environment > deactivate
