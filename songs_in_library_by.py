#!/usr/bin/python3
import json
import sys

if len(sys.argv) not in range(3, 5):
    print("Usage: %s <artist> <library_file> [sort field]" % sys.argv[0])
    exit(1)

libfile = open(sys.argv[2])
library = json.load(libfile)

entries = filter(lambda entry: entry['track']
                 ['artists'][0]['name'] == sys.argv[1], library)

sort_field = "name"
if len(sys.argv) == 4:
    sort_field = sys.argv[3]

entries = sorted(entries, key=lambda entry: entry['track'][sort_field])


for entry in entries:
    print(str(entry['track']['popularity']) + ': "' + entry['track']['name'])
