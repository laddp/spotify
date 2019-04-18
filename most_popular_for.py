#!/usr/bin/python3
import base64
import json
import os
import sys
import requests

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("artist",
                    help="The artist to search for")
parser.add_argument("-c", "--count",
                    help="Number to return (default:25)", type=int, default=25)
parser.add_argument("-v", "--verbose",
                    help="Print progress", action='store_true')
args = parser.parse_args()

client_id = None
client_secret = None

if not client_id:
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
if not client_id:
    raise Exception('No client id')
if not client_secret:
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
if not client_secret:
    raise Exception('No client secret')


def verbose_print(msg, end='\n', flush=False):
    if args.verbose:
        print(msg, end=end, flush=flush)


def get_token_for_client():
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    client_data = client_id + ':' + client_secret
    client_data_encoded = base64.b64encode(client_data.encode('ascii'))
    token_request_header = {
        'Authorization': 'Basic %s' % client_data_encoded.decode('ascii')}
    token_request_body = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(OAUTH_TOKEN_URL, verify=True,
                             headers=token_request_header, data=token_request_body)
    if response.status_code != 200:
        raise Exception(response.reason)
    return response.json()['access_token']


auth_token = get_token_for_client()
header = {
    'Authorization': "Bearer " + auth_token
}


#############################
# Find the best match artist
#############################
artist_url = 'https://api.spotify.com/v1/search?q=' + \
    args.artist + '&type=artist&limit=2'
artist = requests.get(artist_url, headers=header)
artist.raise_for_status()

artist = artist.json()
if artist['artists']['total'] == 0:
    print("No artist found")
    exit(1)
if artist['artists']['items'][0]['name'] != args.artist:
    print("Warning! Artist name doesn't match exactly")
print('Most popular tracks for "' + artist['artists']['items'][0]['name'] +
      '" (popularity ' + str(artist['artists']['items'][0]['popularity']) + ')', end='', flush=True)

artist_id = artist['artists']['items'][0]['id']

############################
# Get all albums for artist
############################
verbose_print("\n\nFetching albums")
albums = []
album_url = 'https://api.spotify.com/v1/artists/' + \
    artist_id + '/albums?country=US&limit=50&include_groups=album,single,compilation'
while album_url:
    response = requests.get(album_url, headers=header).json()
    for item in response['items']:
        albums.append(item['id'])
        verbose_print('#', end='')
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
        response = requests.get(tracks_for_album_url, headers=header).json()
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
    response = requests.get(tracks_data_url, headers=header).json()
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
    print(" from " + str(len(tracks)) + " tracks on " + str(len(albums)) + " albums")
tracks = sorted(tracks, key=lambda item: item['popularity'], reverse=True)
for i in range(min(len(tracks),args.count)):
    track = tracks[i]
    print('[' + str(track['popularity']) + ']: "' + track['name'] +
          '" on "' + track['album']['name'] + '" - ' + track['external_urls']['spotify'])
