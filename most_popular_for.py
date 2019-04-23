#!/usr/bin/python3
import json
import os
import sys
import argparse
import spotutil

parser = argparse.ArgumentParser()
parser.add_argument("artist",
                    help="The artist to search for")
parser.add_argument("-c", "--count",
                    help="Number to return (default:25)", type=int, default=25)
parser.add_argument("-v", "--verbose",
                    help="Print progress", action='store_true')
args = parser.parse_args()


def verbose_print(msg, end='\n', flush=False):
    if args.verbose:
        print(msg, end=end, flush=flush)


auth_header = spotutil.get_auth_header_for_client()

#############################
# Find the best match artist
#############################
artist_url = 'https://api.spotify.com/v1/search?q=' + \
    args.artist + '&type=artist&limit=5'
artists = spotutil.fetch_spotify_url_with_retry(artist_url, auth_header)

if artists['artists']['total'] == 0:
    print("No artist found")
    exit(1)
artist = None
for candidate in artists['artists']['items']:
    if candidate['name'] == args.artist:
        artist = candidate
        break
if not artist:
    print("Warning! Artist name doesn't match exactly")
    artist = artist['artists']['items'][0]
    print("Using " + artist['name'])
    print("Other choices were: ")
    for candidate in artists:
        print(candidate['name'])

print('Most popular tracks for "' +
      artist['name'] + '" (popularity ' + str(artist['popularity']) + ')', end='', flush=True)

############################
# Get all albums for artist
############################
verbose_print("\n\nFetching albums")
albums = []
album_url = 'https://api.spotify.com/v1/artists/' + \
    artist['id'] + '/albums?country=US&limit=50&include_groups=album,single,compilation'
while album_url:
    response = spotutil.fetch_spotify_url_with_retry(album_url, auth_header)
    for item in response['items']:
        albums.append(item['id'])
        verbose_print('#', end='', flush=True)
    album_url = response['next']

verbose_print(" - %s" % len(albums))

############################
# Get tracks for all albums
############################
verbose_print("\nFetching tracks")
track_ids = []
for album in albums:
    verbose_print("#", end='', flush=True)
    tracks_for_album_url = 'https://api.spotify.com/v1/albums/' + \
        album + '/tracks?country=US&limit=50'
    while tracks_for_album_url:
        response = spotutil.fetch_spotify_url_with_retry(
            tracks_for_album_url, auth_header)
        for item in response['items']:
            track_ids.append(item['id'])
            verbose_print(".", end='', flush=True)
        tracks_for_album_url = response['next']
verbose_print(" - %s" % len(track_ids))

##############################
# Re-get tracks for full data
##############################
verbose_print("\nFetching track data")
tracks = []

# fetch in batches of up to 50 - more efficient


def fetch_track_batch(ids):
    verbose_print(str(len(ids))+"...", end='', flush=True)
    query = ','
    tracks_data_url = 'https://api.spotify.com/v1/tracks?country=US&ids=' + \
        query.join(ids)
    response = spotutil.fetch_spotify_url_with_retry(
        tracks_data_url, auth_header)
    for item in response['tracks']:
        tracks.append(item)


count = 0
query_batch = []
for track_id in track_ids:
    query_batch.append(track_id)
    count += 1
    if count == 50:
        fetch_track_batch(query_batch)
        query_batch = []
        count = 0
fetch_track_batch(query_batch)
verbose_print("Done\n")

############################
# Print most popular tracks
############################
if not args.verbose:
    print(" from " + str(len(tracks)) +
          " tracks on " + str(len(albums)) + " albums")
tracks = sorted(tracks, key=lambda item: item['popularity'], reverse=True)
for i in range(min(len(tracks), args.count)):
    track = tracks[i]
    print('[' + str(track['popularity']) + ']: "' + track['name'] +
          '" on "' + track['album']['name'] + '" - ' + track['external_urls']['spotify'])
