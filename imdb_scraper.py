import urllib.request
from bs4 import BeautifulSoup
import json

url = 'http://www.imdb.com/calendar?region=DE&ref_=rlm'

# download URL and extract content
request = urllib.request.Request(url)
html = urllib.request.urlopen(request).read()

# pass HTML to BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
calendar = soup.find('div', attrs={'id':'main'})

dates = calendar.find_all('h4')
links = calendar.find_all('a')

# from each link extract text of link and link itself
upcoming_movies = []
for link in links:
	title = link.text
	url = link['href']
	if not url.startswith('http'):
		url = 'https://www.imdb.com' + url
	movie = {
		'title' :title,
		'url' :url
	}
	upcoming_movies.append(movie)

# write data to json file
with open('imdb_data.json', 'w') as outfile:
	json.dump(upcoming_movies, outfile, indent=4)

# print scraped data
for movie in upcoming_movies:
	print(movie)

