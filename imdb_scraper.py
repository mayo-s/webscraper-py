import urllib.request
from bs4 import BeautifulSoup

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
	movie = {
		'title' :title,
		'url' :url
	}
	upcoming_movies.append(movie)

for movie in upcoming_movies:
	print(movie)

