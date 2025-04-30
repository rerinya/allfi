from tmdbv3api import TMDb
from tmdbv3api import Movie

import os
import django

os.environ.setdefault('DJANGO_SETTING_MODULE', 'mysite.settings')
django.setup()

from allfi.models import Video

tmdb = TMDb()
tmdb.api_key = '3d259872105fab96d72770a252b81ea0'
tmdb.language = 'es'

movie = Movie()

search = movie.search('Alicia en el País de las Maravillas')
id = search[0].id
title = search[0].title #title
overview = search[0].overview #overview
poster_path = "https://image.tmdb.org/t/p/w500/" + search[0].poster_path #poster_path
release_date = search[0].release_date #release_date
vote_average = search[0].vote_average #vote_average
backdrop_path = "https://image.tmdb.org/t/p/w500/" + search[0].backdrop_path #backdrop_path
#print(title)
#    print(res.overview)
#    print(res.poster_path)
#    print(res.release_date)
#    print(res.vote_average)
#    print(res.backdrop_path)

d = movie.details(id)
genres = ''
i = 0;
#get genres
for res in d.genres:
#    print(res['name'])
#    genres = ''.join('' + res['name'])
    if len(d.genres) == i+1:
        genres = genres + res['name']
    else:
        genres = genres + res['name'] + '/'
    i = i + 1

c = movie.credits(id)

cast_list = []
cast_list.append(c.cast[0]['character'] + ": " + c.cast[0]['name'])
cast_list.append(c.cast[1]['character'] + ": " + c.cast[1]['name'])
cast_list.append(c.cast[2]['character'] + ": " + c.cast[2]['name'])
cast = c.cast[0]['character'] + ": " + c.cast[0]['name'] + ";" + c.cast[1]['character'] + ": " + c.cast[1]['name'] \
       + ";" + c.cast[2]['character'] + ": " + c.cast[2]['name']
print(cast)

for res in c.crew:
    if res['job'] == "Director":
        director = res['name']
        #print(director)

m = Video(name=title, url='https://www.youtube.com/embed/eOrNdBpGMv8', description=overview, year=release_date,
        director=director, actor=cast, urlposter=poster_path, urlbackdrop=backdrop_path, genres=genres,
        score=vote_average)
#m.save()
