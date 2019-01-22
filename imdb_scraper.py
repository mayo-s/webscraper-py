import urllib.request
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

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
    title_wrapper = soup.find('div', attrs={'class':'title_wrapper'})
    subtext = title_wrapper.find('div', attrs={'class':'subtext'})

    # extract release date
    release_date_string = subtext.find('a', attrs={'title':'See more release dates'}).text
    # cut off (<country name>)
    release_date_string = release_date_string.split(' ')
    release_date_string = release_date_string[0] + ' ' + release_date_string[1] + ' ' + release_date_string[2]
    # parse date string (d Month YYYY) to datetime object
    release_date = datetime.strptime(release_date_string, '%d %B %Y')

    # extract poster url if existing
    poster_div = soup.find('div', attrs={'class':'poster'})
    if poster_div is not None:
        poster = poster_div.find('img')
        poster_url = poster['src']
    else:
        poster_url = ''

    # extract cast url
    actor_list_wrapper = soup.find('div', attrs={'id':'quicklinksMainSection'})
    actor_list_link = actor_list_wrapper.find('a')
    actor_list_url = actor_list_link['href']
    actor_list_url = 'https://www.imdb.com' + actor_list_url

    # extract cast
    cast_table = soup.find('table', attrs={'class':'cast_list'})
    actors = []
    if cast_table is not None:
        table_rows = cast_table.find_all('tr', attrs={'class': True})
        for row in table_rows:
            name = row.find('td').find_next('td').text
            name = name.replace('\n ','')
            # extract actor id
            actor_link = row.find('a')
            actor_link_url = actor_link['href']
            actor_id = actor_link_url.split('/')[2]
            actor_id = actor_id.replace('nm', '')
            actor = {
                'name': name,
                'id': actor_id
            }
            actors.append(actor)

    # extract genres
    genres = subtext.select('a[href*=genres]')
    genre_text = []
    for genre in genres:
        text = genre.text
        genre_text.append(text)

    # extract rating value of given movie
    rating_wrapper = soup.find('div', attrs={'class':'ratingValue'})
    if rating_wrapper is not None:
        rating_value = rating_wrapper.find('span', attrs={'itemprop':'ratingValue'}).text
        rating_value = float(rating_value)
    else:
        rating_value = None
        
    data = {
        'genres':genre_text,
        'release_date':release_date,
        'poster_url':poster_url,
        'actor_list_url':actor_list_url,
        'actors':actors,
        'rating':rating_value
    }
    return data

def time_format(num):
    return ('%.1f' % num).rstrip('0').rstrip('.')

def print_statistics(upcoming_movies, start, end):
    print ('')
    print ('#################################')
    print ('####      IMDb Scraper       ####')
    text = '#### Movies scraped:    ' + str(len(upcoming_movies)) + '   ####'
    print (text)
    t = time_format(end - start)
    text = '#### Time needed: ' + str(t) + ' secs ####'
    print (text)
    print ('#################################')
    print('')

def scrape():
    start = time.time()
    initial_url = 'http://www.imdb.com/calendar?region=DE' # imdb calendar (Germany)

    # scrape calendar
    print ("IMDb Calendar scraping in progress... ")
    soup = soup_maker(initial_url)
    calendar = soup.find('div', attrs={'id':'main'})
    links = calendar.find_all('a')

    # from each link extract text of link, id and link itself
    print ('Movie scraping in progress... ')
    upcoming_movies = []
    for link in links:
        title = link.text
        url = link['href']

        # extract unique movie id from url (/title/tt<id>/?ref_=rlm)
        imdb_id = url.split('/')[2]
        imdb_id = imdb_id.replace('tt', '')

        # build url
        if not url.startswith('http'):
            url = 'https://www.imdb.com' + url

        # parse each movie
        info = parse_movie(url)

        movie = {
            'imdb_id':imdb_id,
            'title':title,
            'url':url,
            'genres':info.get('genres'),
            'rating':info.get('rating'),
            'release_date':info.get('release_date'),
            'poster_url':info.get('poster_url'),
            'actor_list_url':info.get('actor_list_url'),
            'actor_list':info.get('actors')
        }
        upcoming_movies.append(movie)

    # write data to json file
    with open('imdb_data.json', 'w') as outfile:
        json.dump(upcoming_movies, outfile, indent=4, default=str)
    print('Scraped data dumped into imdb_data.json')

    end = time.time()
    print_statistics(upcoming_movies, start, end)
    return 'imdb_data.json'
