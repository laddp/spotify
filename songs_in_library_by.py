#!/usr/bin/python3
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("artist",
                    help="The artist to search for")
parser.add_argument("library_file",
                    help="The JSON library file to search", type=argparse.FileType('r'))
parser.add_argument("sort_field",
                    help="Field to sort results on (default:name)", nargs="?", default="name",
                    choices=['name','popularity','release_date','duration_ms'])
parser.add_argument("-r", "--reverse",
                    help="Reverse sort order", action="store_true")
args = parser.parse_args()

library = json.load(args.library_file)

entries = filter(lambda entry: entry['track']
                 ['artists'][0]['name'] == args.artist, library)

entries = sorted(
    entries, key=lambda entry: entry['track'][args.sort_field], reverse=args.reverse)

for entry in entries:
    print('"' + entry['track']['name'] + '" on "' + entry['track']
          ['album']['name'] + '" (' + str(entry['track']['popularity']) + ')')
