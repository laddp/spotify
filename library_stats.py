#!/usr/bin/python3
import json
import os
import sys
from datetime import datetime, timedelta

libfile = open(sys.argv[1])
library = json.load(libfile)
print("Total items: " + str(len(library)))

artists = {}
def count_by_artist(entry):
    artist = entry['track']['artists'][0]['name']
    if artist in artists.keys():
        artists[artist] = artists[artist]+1
    else:
        artists[artist] = 1

for entry in library:
    count_by_artist(entry)

print("\nUnique artists: " + str(len(artists)))

artists = sorted(artists.items(), key=lambda tup: tup[1], reverse=True)
print("\nTop artists:")
for i in range(20):
    print(artists[i][0] + ': ' + str(artists[i][1]))


library_by_popularity = sorted(
    library, reverse=True, key=lambda entry: entry['track']['popularity'])

print("\nMost popular:")
for i in range(20):
    track = library_by_popularity[i]['track']
    print(str(track['popularity']) + ': "' + track['name'] +
          '" by ' + track['artists'][0]['name'])

library_witout_zero_popularity = list(
    filter(lambda entry: entry['track']['popularity'] != 0, library_by_popularity))
print("\nLeast popular:")
for i in range(len(library_witout_zero_popularity)-20, len(library_witout_zero_popularity)):
    track = library_witout_zero_popularity[i]['track']
    print(str(track['popularity']) + ': "' + track['name'] +
          '" by ' + track['artists'][0]['name'])

years = {}
last_day = 0
last_week = 0
last_month = 0

now = datetime.today()
day   = now + timedelta(days=-1)
week  = now + timedelta(weeks=-1)
month = now + timedelta(weeks=-4)

firsttrack = [ library[0], datetime.fromisoformat(library[0]['added_at'].strip('Zz')) ]
lasttrack  = [ library[0], datetime.fromisoformat(library[0]['added_at'].strip('Zz')) ]

def count_by_date(entry):
    global last_day
    global last_week
    global last_month
    global firsttrack
    global lasttrack
    d = datetime.fromisoformat(entry['added_at'].strip('Zz'))
    if d > month:
        last_month+=1
        if d > week:
            last_week+=1
            if d > day:
                last_day+=1
    if d.year in years.keys():
        years[d.year] = years[d.year]+1
    else:
        years[d.year] = 1
    
    if d < firsttrack[1]:
        firsttrack = [ entry, d]
    if d > lasttrack[1]:
        lasttrack = [ entry , d]

for entry in library:
    count_by_date(entry)

print("\nSongs added in:")
print("last day: " + str(last_day))
print("last week: " + str(last_week))
print("last month: " + str(last_month))
for entry in sorted(years.items(), reverse=True):
    print(str(entry[0]) + ': ' + str(entry[1]))

print("\nFirst add: " + firsttrack[0]['track']['name'] + 
      ' by ' + firsttrack[0]['track']['artists'][0]['name'] +
      ' at ' + firsttrack[1].isoformat())
print("Last add: " + lasttrack[0]['track']['name'] + 
      ' by ' + lasttrack[0]['track']['artists'][0]['name'] +
      ' at ' + lasttrack[1].isoformat())
