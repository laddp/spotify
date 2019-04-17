#!/usr/bin/python3
import base64
import json
import os
import datetime
import sys
import requests

OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

client_id = None
client_secret = None

if len(sys.argv) not in range(2,4):
    print(len(sys.argv))
    print("Usage: %s <refresh_token> [output_dir]" % sys.argv[0])
    raise Exception("Missing argument(s)")

refresh_token = sys.argv[1]
output_dir = ''
if len(sys.argv) == 3:
    output_dir = sys.argv[2] + '/'

if not client_id:
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
if not client_id:
    raise Exception('No client id')
if not client_secret:
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
if not client_secret:
    raise Exception('No client secret')


def get_token_from_refresh_token(refresh_token):
    client_data = client_id + ':' + client_secret
    client_data_encoded = base64.b64encode(client_data.encode('ascii'))
    token_request_header = {
        'Authorization': 'Basic %s' % client_data_encoded.decode('ascii')}
    token_request_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(OAUTH_TOKEN_URL, verify=True,
                             headers=token_request_header, data=token_request_body)
    if response.status_code != 200:
        raise Exception(response.reason)
    return response.json()['access_token']


auth_token = get_token_from_refresh_token(refresh_token)
header = {
    'Authorization': "Bearer " + auth_token
}
url = 'https://api.spotify.com/v1/me/tracks?market=US&limit=50'
results = []
count = 0

print("Getting library tracks")
while url:
    response = requests.get(url, headers=header).json()
    for item in response['items']:
        results.append(item)
        print('.', end='')
        count += 1
    url = response['next']
    print(" - ", count)

filename = str(datetime.date.today()) + '.json'
with open(output_dir + filename, 'w') as outfile:
    json.dump(results, outfile)
