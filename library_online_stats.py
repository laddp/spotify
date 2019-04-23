#!/usr/bin/python3
import json
import os
import sys
import argparse
import requests
import spotutil

parser = argparse.ArgumentParser()
parser.add_argument("library_file",
                    help="The JSON library file to analyze", type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose",
                    help="Print progress", action='store_true')
args = parser.parse_args()


def verbose_print(msg, end='\n', flush=False):
    if args.verbose:
        print(msg, end=end, flush=flush)


library = json.load(args.library_file)

artists = {}
for track in library:
    for artist in track['track']['artists']:
        if artist['id'] not in artists:
            artists[artist['id']] = {'name': artist['name'], 'count': 1}
        else:
            artists[artist['id']]['count'] += 1

auth_header = spotutil.get_auth_header_for_client()

verbose_print("Collected " + str(len(artists)) + " artists")


def fetch_artist_batch(ids):
    global artists
    verbose_print(str(len(ids))+"...", end='', flush=True)
    artists_url = 'https://api.spotify.com/v1/artists?ids='
    query = ','
    artists_url = 'https://api.spotify.com/v1/artists?ids=' + query.join(ids)
    response = requests.get(artists_url, headers=auth_header).json()
    for item in response['artists']:
        artists[item['id']]['detail'] = item


count = 0
query_batch = []
for artist_id in artists.keys():
    query_batch.append(artist_id)
    count += 1
    if count == 50:
        fetch_artist_batch(query_batch)
        query_batch = []
        count = 0
fetch_artist_batch(query_batch)

genres = {}
weighted_genres = {}
# count artist genres
for artist in artists.values():
    for genre in artist['detail']['genres']:
        if genre not in genres:
            genres[genre] = 1
            weighted_genres[genre] = artist['count']
        else:
            genres[genre] += 1
            weighted_genres[genre] += artist['count']

genres = sorted(genres.items(), key=lambda tup: tup[1], reverse=True)
print("\nTop genres:")
for i in range(50):
    print(genres[i][0] + ': ' + str(genres[i][1]))

weighted_genres = sorted(weighted_genres.items(),
                         key=lambda tup: tup[1], reverse=True)
print("\nTop genres (weighted by tack count):")
for i in range(50):
    print(weighted_genres[i][0] + ': ' + str(weighted_genres[i][1]))


artists_by_popularity = sorted(
    artists.values(), reverse=True, key=lambda artist: artist['detail']['popularity'])

print("\nMost popular artists in your library:")
for i in range(20):
    print(str(artists_by_popularity[i]['detail']['popularity']) +
     ': ' + artists_by_popularity[i]['detail']['name'])

print("\nLeast popular artists in your library:")
for i in range(len(artists_by_popularity)-20, len(artists_by_popularity)):
    print(str(artists_by_popularity[i]['detail']['popularity']) +
     ': ' + artists_by_popularity[i]['detail']['name'])

artists_by_followers = sorted(
    artists.values(), reverse=True, key=lambda artist: artist['detail']['followers']['total'])
print("\nMost followed artists in your library:")
for i in range(20):
    print("{:,}".format(artists_by_followers[i]['detail']['followers']['total']) +
     ': ' + artists_by_followers[i]['detail']['name'])

print("\nLeast followed artists in your library:")
for i in range(len(artists_by_popularity)-20, len(artists_by_popularity)):
    print("{:,}".format(artists_by_followers[i]['detail']['followers']['total']) +
     ': ' + artists_by_followers[i]['detail']['name'])
