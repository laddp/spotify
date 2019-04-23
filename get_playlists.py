#!/usr/bin/python3
import json
import datetime
import sys
import argparse
import spotutil

parser = argparse.ArgumentParser()
parser.add_argument("refresh_token",
                    help="Your personal Spotify refresh token")
parser.add_argument("output_dir", nargs="?",
                    help="Output directory", default='.')
parser.add_argument("-q", "--quiet",
                    help="No output", action='store_true')
args = parser.parse_args()

# open file now - fail fast :)
filename = args.output_dir + '/' + \
    str(datetime.date.today()) + '-playlists.json'
outfile = open(filename, 'w')

auth_header = spotutil.get_auth_header_from_refresh_token(args.refresh_token)

playlists_url = 'https://api.spotify.com/v1/me/playlists'
basic_playlists = []
while playlists_url:
    response = spotutil.fetch_spotify_url_with_retry(
        playlists_url, auth_header)
    for item in response['items']:
        basic_playlists.append(item)
    playlists_url = response['next']

if not args.quiet:
    print("Retrieved " + str(len(basic_playlists)) + " playlists")

trackcount = 0
playlists = []
for playlist in basic_playlists:
    count = 0
    if not args.quiet:
        print(playlist['name'] + " (" + playlist['owner']
              ['display_name'] + ")", end='')

    # Have to re-fetch playlist, becaue playlists URL returns only basic objects
    # Doesn't include:
    #  - description
    #  - followers
    playlist_url = "https://api.spotify.com/v1/playlists/" + \
        playlist['id'] + "?market=US"
    response = spotutil.fetch_spotify_url_with_retry(playlist_url, auth_header)
    playlist = response

    # playlist fetch only returns basic track objects
    # fetch full track objects and replace
    pl_tracks_url = playlist['tracks']['href']
    playlist['tracks']['items'] = []
    playlist['tracks']['limit'] = 0
    playlist['tracks']['next'] = None
    while pl_tracks_url:
        response = spotutil.fetch_spotify_url_with_retry(
            pl_tracks_url, auth_header)
        for item in response['items']:
            playlist['tracks']['items'].append(item)
        count += len(response['items'])
        if not args.quiet:
            print("...%s" % str(count), end='', flush=True)
        pl_tracks_url = response['next']
        if pl_tracks_url:
            pl_tracks_url += "&market=US"
    playlists.append(playlist)
    trackcount += count
    print()

if not args.quiet:
    print("\nRetrieved " + str(len(playlists)) +
          " playlists with " + str(trackcount) + " tracks, writing to " + filename)

filename = str(datetime.date.today()) + '.json'
json.dump(playlists, outfile)
