import urllib.request
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

start = time.time()
initial_url = 'http://www.imdb.com/calendar?region=DE&ref_=rlm' # imdb calendar (Germany)

def soup_maker(url):
    # download URL and extract content
    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()
    # pass HTML to BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# scrape calendar
print ("IMDb Calendar scraping in progress... ")
soup = soup_maker(initial_url)
calendar = soup.find('div', attrs={'id':'main'})
links = calendar.find_all('a')

# extract specific movie information
def parse_movie(url):
    soup = soup_maker(url)
    title_wrapper = soup.find('div', attrs={'class':'title_wrapper'})
    # rating = title_wrapper.find('span', attrs={'itemprop':'ratingValue'}).text
    subtext = title_wrapper.find('div', attrs={'class':'subtext'})
    # not all movies have a specified length
    # length = subtext.find('time').text
    # not all movies have a rating yet
    # rating = ...
    release_date_string = subtext.find('a', attrs={'title':'See more release dates'}).text
    # cut off (<country name>)
    release_date_string = release_date_string.split(' ')
    release_date_string = release_date_string[0] + ' ' + release_date_string[1] + ' ' + release_date_string[2]
    # parse date string (d Month YYYY) to datetime object
    release_date = datetime.strptime(release_date_string, '%d %B %Y')
    poster_div = soup.find('div', attrs={'class':'poster'})
    if poster_div is not None:
        poster = poster_div.find('img')
        poster_url = poster['src']
    else:
        poster_url = ''

    # extract Cast link
    actor_list_wrapper = soup.find('div', attrs={'id':'quicklinksMainSection'})
    actor_list_link = actor_list_wrapper.find('a')
    actor_list_url = actor_list_link['href']
    actor_list_url = 'https://www.imdb.com' + actor_list_url

    genres = subtext.select('a[href*=genres]')
    genre_text = []
    for genre in genres:
        text = genre.text
        genre_text.append(text)
        data = {
        #    'rating':rating,
            'genres':genre_text,
            'release_date':release_date,
            'poster_url':poster_url,
            'actor_list_url':actor_list_url
        #   'length':length
        }
    return data

def parse_cast(url):
    soup = soup_maker(url)
    cast_table = soup.find('table', attrs={'class':'cast_list'})
    actors = cast_table.select('a[href*=name]')

    cast_names = []
    for actor in actors:
        name = actor.text
        cast_names.append(name)
    return cast_names

# from each link extract text of link, id and link itself
print ('Movie scraping in progress... ')
upcoming_movies = []
for link in links:
    title = link.text
    url = link['href']

    #extract unique movie id from url (/title/tt<id>/?ref_=rlm)
    imdb_id = url.split('/')[2]
    imdb_id = imdb_id.replace('tt', '')

    if not url.startswith('http'):
        url = 'https://www.imdb.com' + url
    info = parse_movie(url)
    cast_url = info.get('actor_list_url')
    movie = {
        'imdb_id':imdb_id,
        'title':title,
        'url':url,
        'genres':info.get('genres'),
        # 'length':info.get('length'),
        # 'rating':info.get('rating'),
        'release_date':info.get('release_date'),
        'poster_url':info.get('poster_url'),
        'actor_list_url':info.get('actor_list_url'),
        'actor_list':parse_cast(cast_url)
    }
    upcoming_movies.append(movie)

# write data to json file
with open('imdb_data.json', 'w') as outfile:
    json.dump(upcoming_movies, outfile, indent=4, default=str)
print('Scraped data dumped into imdb_data.json')

def time_format(num):
    return ('%.1f' % num).rstrip('0').rstrip('.')

def print_statistics():
    print ('')
    print ('#################################')
    print ('####      IMDb Scraper       ####')
    text = '#### Movies scraped:    ' + str(len(upcoming_movies)) + '   ####'
    print (text)
    end = time.time()
    t = time_format(end - start)
    text = '#### Time needed: ' + str(t) + ' secs ####'
    print (text)
    print ('#################################')
    print('')

# print scraped data
def print_all_data():
    for movie in upcoming_movies:
        print('')
        print(movie.get('title'))
        print(movie.get('url'))
        print(movie.get('genres'))
        print(movie.get('release_date'))
        # print(movie.get('rating'))

print_statistics()
# print_all_data()
