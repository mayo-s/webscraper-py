import urllib.request
from bs4 import BeautifulSoup
import json
import time

start = time.time()
initial_url = 'http://www.imdb.com/calendar?region=DE&ref_=rlm'

def soup_maker(url):
# download URL and extract content
	request = urllib.request.Request(url)
	html = urllib.request.urlopen(request).read()

	# pass HTML to BeautifulSoup
	soup = BeautifulSoup(html, 'html.parser')
	return soup

# extract specific movie information
def parse_movie(url):
	soup = soup_maker(url)
	title_wrapper= soup.find('div', attrs={'class':'title_wrapper'})
	subtext = title_wrapper.find('div', attrs={'class':'subtext'})
	# not all movies have a specified length
	# length = subtext.find('time').text
	release_date = subtext.find('a', attrs={'title':'See more release dates'}).text
	genres = subtext.select('a[href*=genres]')	
	genre_text = []
	for genre in genres:
		text = genre.text
		genre_text.append(text[1:-1])
	data = {
		'genres':genre_text,
		'release_date':release_date[:16],
	#	'length':length
	}
	return data

# scrape calendar
soup = soup_maker(initial_url)
calendar = soup.find('div', attrs={'id':'main'})
links = calendar.find_all('a')

# from each link extract text of link and link itself
upcoming_movies = []
for link in links:
	title = link.text
	url = link['href']
	if not url.startswith('http'):
		url = 'https://www.imdb.com' + url
	info = parse_movie(url)
	movie = {
		'title':title,
		'url':url,
		'genres':info.get('genres'),
	#	'length':info.get('length'),
		'release_date':info.get('release_date')
	}
	upcoming_movies.append(movie)

# write data to json file
with open('imdb_data.json', 'w') as outfile:
	json.dump(upcoming_movies, outfile, indent=4)

def time_format(num):
    return ('%.1f' % num).rstrip('0').rstrip('.')

# print scraped data
print ('')
print ('#################################')
print ('####      IMDb Scraper       ####')
text = '#### Movies scraped:    ' + str(len(upcoming_movies)) + '   ####'
print (text)
end = time.time()
time = time_format(end - start)
text = '#### Time needed: ' + str(time) + ' secs ####'
print (text)
print ('#################################')

for movie in upcoming_movies:
	print('')
	print(movie.get('title'))
	print(movie.get('url'))
	print(movie.get('genres'))
	print(movie.get('release_date'))


