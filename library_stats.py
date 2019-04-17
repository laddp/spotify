#!/usr/bin/python3
import json
import os
import sys

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
