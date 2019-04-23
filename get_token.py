#!/usr/bin/python3
import os
import requests
import six.moves.urllib.parse as urllibparse
import json
import spotutil

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
redirect_url = 'http://localhost/'
protected_url = 'https://api.spotify.com/v1/'

spotutil.get_client_id_and_secret()
client_id = spotutil.client_id
client_secret = spotutil.client_secret


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
    token_request_header = spotutil.get_auth_header_for_client()
    token_request_body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url
    }
    response = requests.post(OAUTH_TOKEN_URL, verify=True,
                             headers=token_request_header, data=token_request_body)
    if not response.ok():
        response.raise_for_status()
    return response.json()


code = request_auth_code()
tokens = get_tokens_from_authcode(code)
print("Your refresh token is: " + tokens['refresh_token'])
