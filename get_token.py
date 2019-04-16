#!/usr/bin/python3
import os
import base64
import requests
import six.moves.urllib.parse as urllibparse
import json

client_id = None
client_secret = None

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
redirect_url = 'http://localhost/'
protected_url = 'https://api.spotify.com/v1/'

if not client_id:
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
if not client_id:
    raise Exception('No client id')
if not client_secret:
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
if not client_secret:
    raise Exception('No client secret')


def request_auth_code():
    auth_request = {
        'client_id': client_id,
        'client_secret': client_secret,
        'response_type': 'code',
        'redirect_uri': redirect_url,
        'scope': 'user-library-read playlist-read-private playlist-read-collaborative'
    }
    auth_url = OAUTH_AUTHORIZE_URL + '?' + urllibparse.urlencode(auth_request)
    try:
        import webbrowser
        webbrowser.open(auth_url)
        print("Opened %s in your browser" % auth_url)
    except:
        print("Please navigate here: %s" % auth_url)

    try:
        response = raw_input("Enter the URL you were redirected to: ")
    except NameError:
        response = input("Enter the URL you were redirected to: ")

    code = response.split("?code=")[1].split("&")[0]
    return code


def get_tokens_from_authcode(code):
    client_data = client_id + ':' + client_secret
    client_data_encoded = base64.b64encode(client_data.encode('ascii'))
    token_request_header = {
        'Authorization': 'Basic %s' % client_data_encoded.decode('ascii')}
    token_request_body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url
    }
    response = requests.post(OAUTH_TOKEN_URL, verify=True,
                             headers=token_request_header, data=token_request_body)
    if response.status_code != 200:
        raise Exception(response.reason)
    return response.json()


code = request_auth_code()
tokens = get_tokens_from_authcode(code)
print("Your refresh token is: " + tokens['refresh_token'])
