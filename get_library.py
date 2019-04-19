#!/usr/bin/python3
import json
import datetime
import sys
import requests
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
filename = args.output_dir + '/' + str(datetime.date.today()) + '.json'
outfile = open(filename, 'w')

auth_header = spotutil.get_auth_header_from_refresh_token(args.refresh_token)

url = 'https://api.spotify.com/v1/me/tracks?market=US&limit=50'
results = []
count = 0
while url:
    response = requests.get(url, headers=auth_header).json()
    for item in response['items']:
        results.append(item)
        count += 1
    url = response['next']
    if not args.quiet:
        print("...%s" % count, end='', flush=True)

if not args.quiet:
    print("\nRetrieved " + str(len(results)) + " tracks, writing to " + filename)
filename = str(datetime.date.today()) + '.json'
json.dump(results, outfile)
