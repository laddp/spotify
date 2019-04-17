# spotify
Some spotify API hacking stuff


**```get_library.py```**: Save your Spotify library off as a JSON file

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
7. Run ```get_library.py``` with that token as command arugment (and optional output directory)
8. The json contents of your Spotify library will be saved as yyyy-mm-dd.json

Repeat steps 3,4,7 as necessary to back up your library

Also - the results are packed and hard to read, so use ```cat yyyy-mm-dd.json | python -m json.tool | more``` to view formatted

Add this to your crontab to collect your library weekly:
```
@weekly SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=xxx /home/pladd/bin/get_library xxxxxxxxx /home/pladd/spotify/
```

**```get_token.py```**: Service routine to get a reusable refresh token

Module requirements: python3-requests

**```library_stats.py```**: Compute some statistics about your library
* Total number of tacks
* Number of unique artists
* Most frequent artists
* Most popular tracks
* Least popular tracks
* Add counts by day, week, month, and year
* First and last tracks added


Sample output (FYI popularity numbers are dynamic based on current trends)
```
Total items: 4835

Unique artists: 980

Top artists:
Dream Theater: 242
Pink Floyd: 147
John Williams: 78
Jimmy Buffett: 72
Leonard Bernstein: 60
Led Zeppelin: 52
Metallica: 48
Rush: 46
Fleetwood Mac: 45
The Smashing Pumpkins: 42
Van Halen: 38
Yes: 38
Eric Clapton: 36
U2: 36
Eagles: 35
Madonna: 34
The Hello Strangers: 32
Rage Against The Machine: 32
Garbage: 31
Def Leppard: 29

Most popular:
89: "Believer" by Imagine Dragons
88: "Shape of You" by Ed Sheeran
88: "Thunder" by Imagine Dragons
86: "Africa" by Toto
85: "I'm Yours" by Jason Mraz
85: "Stressed Out" by Twenty One Pilots
85: "Take on Me" by a-ha
84: "Nevermind" by Dennis Lloyd
84: "Back In Black" by AC/DC
84: "Highway to Hell" by AC/DC
84: "Hey, Soul Sister" by Train
84: "Something Just Like This" by The Chainsmokers
84: "Do I Wanna Know?" by Arctic Monkeys
84: "Pumped Up Kicks" by Foster The People
84: "The Scientist" by Coldplay
84: "Hey, Soul Sister" by Train
84: "In The End" by Linkin Park
83: "Heathens" by Twenty One Pilots
83: "Without Me" by Eminem
83: "Sweet Home Alabama" by Lynyrd Skynyrd

Least popular:
2: "Que Sera, Sera" by The Hello Strangers
2: "High Hopes (Edit) [2011 Remastered Version]" by Pink Floyd
1: "Rockaway Beach - Remastered" by Ramones
1: "What You Don't Know (feat. Jim Lauderdale)" by The Hello Strangers
1: "Ruined" by The Hello Strangers
1: "Holy Unholy" by The Hello Strangers
1: "March from "1941"" by Life Guards Band
1: "Tepepa - Viva la Revolucion - Version 2" by Ennio Morricone
1: "On the Town : New York, New York" by Leonard Bernstein
1: "America" by Leonard Bernstein
1: "Monkey On My Back" by Austin Lounge Lizards
1: "Last Words" by Austin Lounge Lizards
1: "Rock Of Ages (2012)" by Def Leppard
1: "Hysteria 2013 (Re-Recorded Version) - Single" by Def Leppard
1: "Layla (Piano Exit)" by Derek & The Dominos
1: "The Same Routine" by The Hello Strangers
1: "Poor Dear" by The Hello Strangers
1: "Ruined" by The Hello Strangers
1: "Holy Unholy" by The Hello Strangers
1: "Time (Edit) [2011 Remastered Version]" by Pink Floyd

Songs added in:
last day: 7
last week: 7
last month: 8
2019: 10
2018: 408
2017: 720
2016: 2813
2015: 677
2014: 207

First add: The Enemy Inside - Live From The Boston Opera House by Dream Theater at 2014-10-11T16:39:11
Last add: Jonas & Ezekial by Indigo Girls at 2019-04-16T19:35:05
```