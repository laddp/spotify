# spotify
Some spotify API hacking stuff


**get_library.py** Save your Spotify library off as a JSON file

At some point, I spent a bunch of time adding tracks I liked to a music service.  That music service tanked suddenly
one day with a "sorry we got sued into oblivion" message, so all that effort was lost.  While I don't think Spotify
is going anywhere, that still bugged me, so I resolved to save my list of liked songs somewhere safe.  This is the
script I wrote to do that.

How to use:

1. Get a spotify app client ID and secret at https://developer.spotify.com/dashboard/applications
2. Add "http://localhost/" to the redirect URLs allowed for your app
3. ```export SPOTIFY_CLIENT_ID=xxxx```
4. ```export SPOTIPY_CLIENT_SECRET=xxxx```
5. One time: run ```get_token.py```
   It will:
   * Open a browser window where spotify will ask you for permissions
   * Redirect you to localhost/?somehugelongthing
6. Paste that redirect URL back into get_token.py, which will spit out a "refresh token"
7. Run ```get_library.py``` with that token as command arugment
8. The json contents of your Spotify library will be saved as yyyy-mm-dd.json

Repeat steps 3,4,7 as necessary to back up your library

Also - the results are packed and hard to read, so use ```cat yyyy-mm-dd.json | python -m json.tool | more``` to view formatted

**get_token.py** Service routine to get a reusable refresh token

