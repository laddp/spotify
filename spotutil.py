#!/usr/bin/python3
import os
import base64
import time
import requests


client_id = None
client_secret = None


def get_client_id_and_secret():
    global client_id, client_secret
    if not client_id:
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
    if not client_id:
        raise Exception('No client id - did you export SPOTIFY_CLIENT_ID ?')
    if not client_secret:
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not client_secret:
        raise Exception(
            'No client secret - did you export SPOTIFY_CLIENT_SECRET ?')


def client_auth_header():
    global client_id, client_secret
    get_client_id_and_secret()
    client_data = client_id + ':' + client_secret
    client_data_encoded = base64.b64encode(client_data.encode('ascii'))
    return {
        'Authorization': 'Basic %s' % client_data_encoded.decode('ascii')
    }


def get_auth_header_for_client():
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    get_client_id_and_secret()
    token_request_header = client_auth_header()
    token_request_body = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(OAUTH_TOKEN_URL, verify=True,
                             headers=token_request_header, data=token_request_body)
    if response.status_code != 200:
        raise Exception(response.reason)
    return {
        'Authorization': "Bearer " + response.json()['access_token']
    }


def get_auth_header_from_refresh_token(refresh_token):
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    token_request_header = client_auth_header()
    token_request_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(OAUTH_TOKEN_URL, verify=True,
                             headers=token_request_header, data=token_request_body)
    if response.status_code != 200:
        raise Exception(response.reason)
    return {
        'Authorization': "Bearer " + response.json()['access_token']
    }


def fetch_spotify_url_with_retry(url, auth_header):
    while True:
        response = requests.get(url, headers=auth_header)
        if not response.ok:
            if response.status_code == 429:  # rate limit
                time.sleep(int(response.headers['Retry-After']))
                continue
            else:
                response.raise_for_status()
        else:
            return response.json()
