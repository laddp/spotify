# spotify

Some [Spotify API](https://developer.spotify.com/documentation/web-api/reference/) hacking stuff

# Setup

**To run any of the online apps you need:**

1. Get a spotify app client ID and secret at <https://developer.spotify.com/dashboard/applications>
2. Add "<http://localhost/>" to the redirect URLs allowed for your app
3. `export SPOTIFY_CLIENT_ID=xxxx`
4. `export SPOTIPY_CLIENT_SECRET=xxxx`

Most online apps also need a "refresh token":

1. A one-time run of `get_token.py` gets you a "refresh token" that can be reused indefinitely [(see below)](#get_tokenpy-service-routine-to-get-a-reusable-refresh-token)

# `get_library.py`: Save your Spotify library off as a JSON file

At some point, I spent a bunch of time adding tracks I liked to a music service.
That music service tanked suddenly one day with a "sorry we got sued into oblivion"
message, so all that effort was lost. While I don't think Spotify is going anywhere,
that still bugged me, so I resolved to save my list of liked songs somewhere safe.
This is the script I wrote to do that.

Stores the contents of your Spotify library as a JSON file `yyyy-mm-dd-library.json`

Usage:

```
get_library.py [-h] [-q] refresh_token [output_dir]

positional arguments:
  refresh_token  Your personal Spotify refresh token
  output_dir     Output directory

optional arguments:
  -h, --help     show this help message and exit
  -q, --quiet    No output
```

Sample output:

```
./get_library.py $SPOTIFY_TOKEN
...50...100...150...200...250...300...350...400...450...500...550...600...650
...700...750...800...850...900...950...1000...1050...1100...1150...1200...1250
...1300...1350...1400...1450...1500...1550...1600...1650...1700...1750...1800
...1850...1900...1950...2000...2050...2100...2150...2200...2250...2300...2350
...2400...2450...2500...2550...2600...2650...2700...2750...2800...2850...2900
...2950...3000...3050...3100...3150...3200...3250...3300...3350...3400...3450
...3500...3550...3600...3650...3700...3750...3800...3850...3900...3950...4000
...4050...4100...4150...4200...4250...4300...4350...4400...4450...4500...4550
...4600...4650...4700...4750...4800...4850...4900...4950...4983
Retrieved 4983 tracks, writing to ./2019-04-19.json
```

Results are packed and hard to read, so use `cat yyyy-mm-dd.json | python -m json.tool | more` to view them in human readable form

Add this to your crontab to collect your library weekly:

```
@weekly SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=xxx /home/pladd/bin/get_library xxxxxxxxx /home/pladd/spotify/
```

# `get_playlists.py`: Save your Spotify playlist contents off as a JSON file

Stores the contents of your Spotify playlists as JSON file `yyyy-mm-dd-playlists.json`

Usage:

```
get_playlists.py [-h] [-q] refresh_token [output_dir]

positional arguments:
  refresh_token  Your personal Spotify refresh token
  output_dir     Output directory

optional arguments:
  -h, --help     show this help message and exit
  -q, --quiet    No output
  ```

Sample output:
```
./get_playlists.py $SPOTIFY_TOKEN
Retrieved 9 playlists
Sludge (Spotify)...57
Discover Weekly (Spotify)...30
My Shazam Tracks (Patrick Ladd)...100...200...300...400...500...592
Matrix Soundtrack (Tim Ljunggren)...33
Meditations (Patrick Ladd)...6
Star Wars I-VIII Complete (NewJT)...100...168
Liked from Radio (Patrick Ladd)...16
Windows Media Player (Patrick Ladd)...0
iTunes (Patrick Ladd)...0

Retrieved 9 playlists with 902 tracks, writing to ./2019-04-22-playlists.json
```

# `get_token.py`: Service routine to get a reusable refresh token

The online apps require a "refresh token" to give permission to query your data. You'll need to run this once to grant proper permissions.

1. Run `get_token.py` It will:

  - Open a browser window where spotify will ask you for permissions
  - Redirect you to localhost/?somehugelongthing

2. Paste that redirect URL back into get_token.py, which will spit out a "refresh token"

# `most_popular_for.py`: Show most popular songs for an artist

(Online - app tokens only)

Spotify web UI only shows the 5 most popular now, and [their API](https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/) only returns 10 (and isn't configurable...)

Usage:

```
most_popular_for.py [-h] [-c COUNT] [-v] artist

positional arguments:
  artist                The artist to search for

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number to return (default:25)
  -v, --verbose         Print progress
```

Sample output:

```
./most_popular_for.py "U2" --count 5
Most popular tracks for "U2" (popularity 81) from 695 tracks on 68 albums
[79]: "With Or Without You - Remastered" on "The Joshua Tree (Super Deluxe)" - https://open.spotify.com/track/6ADSaE87h8Y3lccZlBJdXH
[77]: "One" on "Achtung Baby (Deluxe Edition)" - https://open.spotify.com/track/3G69vJMWsX6ZohTykad2AU
[76]: "I Still Haven't Found What I'm Looking For" on "The Joshua Tree (Super Deluxe)" - https://open.spotify.com/track/6wpGqhRvJGNNXwWlPmkMyO
[71]: "Sunday Bloody Sunday - Remastered 2008" on "War (Remastered)" - https://open.spotify.com/track/6C4LXC9UFH1IKiHYOp0BiJ
[66]: "Where The Streets Have No Name - Remastered" on "The Joshua Tree (Super Deluxe)" - https://open.spotify.com/track/4qgZs0RNjdzKAS22lP0QjY
```

```
./most_popular_for.py "U2" --count 5 -v
Most popular tracks for "U2" (popularity 81)

Fetching albums
#################################################################### - 68

Fetching tracks
#.................#...........#.....................#...........#............#.
.......#..........#...........#............#...........#...........#...........
.#..........#..........................#............#.................#........
...#............................#..............................................
...#..........................#..........#..........#..........#..........#....
..................#............................#...........#...........#.......
..................#...........#....#....#...#.#.#.#...#.#.#.#.#..#.#.#..#.#.#..
...#...#.#...#...#...#.#..#....#.....#....#....#..................#............
...............#.#...............................#................#............
..................#...............#........#........ - 695

Fetching track data
50...50...50...50...50...50...50...50...50...50...50...50...50...45...Done

[79]: "With Or Without You - Remastered" on "The Joshua Tree (Super Deluxe)" - https://open.spotify.com/track/6ADSaE87h8Y3lccZlBJdXH
[77]: "One" on "Achtung Baby (Deluxe Edition)" - https://open.spotify.com/track/3G69vJMWsX6ZohTykad2AU
[76]: "I Still Haven't Found What I'm Looking For" on "The Joshua Tree (Super Deluxe)" - https://open.spotify.com/track/6wpGqhRvJGNNXwWlPmkMyO
[71]: "Sunday Bloody Sunday - Remastered 2008" on "War (Remastered)" - https://open.spotify.com/track/6C4LXC9UFH1IKiHYOp0BiJ
[66]: "Where The Streets Have No Name - Remastered" on "The Joshua Tree (Super Deluxe)" - https://open.spotify.com/track/4qgZs0RNjdzKAS22lP0QjY
```

# `songs_in_library_by.py`: Search library for songs by an artist

(Offline - no refresh token required)

Usage:

```
songs_in_library_by.py [-h] [-r]
                              artist library_file
                              [{name,popularity,release_date,duration_ms}]

positional arguments:
  artist                The artist to search for
  library_file          The JSON library file to search
  {name,popularity,release_date,duration_ms}
                        Field to sort results on (default:name)

optional arguments:
  -h, --help            show this help message and exit
  -r, --reverse         Reverse sort order
```

'popularity' is a good sort field

Sample output:

```
./songs_in_library_by.py "Puddle Of Mudd" 2019-04-17.json popularity -r
"Blurry" on "Come Clean" (67)
"Blurry" on "Come Clean" (67)
"She Hates Me" on "Come Clean" (66)
"She Hates Me" on "Come Clean" (66)
"Psycho" on "Famous" (60)
"Control" on "Come Clean" (60)
"Control" on "Come Clean" (60)
"Famous" on "Famous" (54)
"She Hates Me" on "Best Of" (53)
"Drift And Die" on "Come Clean" (53)
"Psycho" on "Best Of" (50)
"Away From Me" on "Best Of" (14)
"Famous" on "Best Of" (2)
```

# `library_stats.py`: Compute some statistics about your library

(Offline - no refresh token required)

Compute some nerdy stats on your library:

- Total number of tacks
- Number of unique artists
- Most frequent artists
- Most popular tracks
- Least popular tracks
- Add counts by day, week, month, and year
- First and last tracks added

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

# `library_online_stats.py`: Compute some online statistics about your library

(Online - app tokens only)

Compute some more nerdy stats on your library:

- Genres by artist
- Genres weighted by track count
- Most / least popular artists
- Most / least followed artists

Usage:
```
library_online_stats.py [-h] [-v] library_file

positional arguments:
  library_file   The JSON library file to analyze

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Print progress
  ```

Sample output:
```
./library_online_stats.py 2019-04-23-library.json -v
Collected 1322 artists
50...50...50...50...50...50...50...50...50...50...50...50...50...50...
50...50...50...50...50...50...50...50...50...50...50...50...22...
Top genres:
rock: 277
pop rock: 157
mellow gold: 148
album rock: 148
soft rock: 146
post-grunge: 145
new wave pop: 139
classic rock: 132
alternative metal: 109
hard rock: 106
dance rock: 105
alternative rock: 94
nu metal: 89
modern rock: 88
new wave: 86
folk rock: 84
art rock: 82
new romantic: 81
permanent wave: 71
adult standards: 65
dance pop: 65
christmas: 63
soul: 61
blues-rock: 57
disco: 56
funk: 56
pop: 56
rap rock: 54
folk-pop: 54
southern rock: 51
motown: 49
roots rock: 48
psychedelic rock: 46
quiet storm: 44
folk: 44
synthpop: 43
indie rock: 43
metal: 41
neo mellow: 41
classic soul: 39
pop punk: 38
lilith: 37
glam metal: 35
indie pop: 35
brill building pop: 34
lounge: 34
heartland rock: 34
grunge: 34
europop: 34
garage rock: 33

Top genres (weighted by tack count):
rock: 2415
album rock: 1334
classic rock: 1237
post-grunge: 961
soft rock: 957
mellow gold: 955
pop rock: 928
hard rock: 895
alternative metal: 731
permanent wave: 660
art rock: 651
alternative rock: 619
metal: 589
folk rock: 578
new wave pop: 555
nu metal: 535
progressive rock: 510
psychedelic rock: 414
modern rock: 411
dance rock: 406
progressive metal: 354
new wave: 341
blues-rock: 335
christmas: 328
adult standards: 308
southern rock: 305
neo classical metal: 304
new romantic: 303
symphonic rock: 272
roots rock: 269
rap rock: 269
heartland rock: 266
pop punk: 253
dance pop: 248
soul: 231
folk-pop: 231
glam metal: 200
folk: 196
funk: 190
motown: 189
rap metal: 186
lilith: 174
disco: 171
neo mellow: 170
classical performance: 167
grunge: 163
funk metal: 154
pop: 150
lounge: 145
vocal jazz: 145

Most popular artists in your library:
94: Queen - https://open.spotify.com/artist/1dfeR4HaWDbWqFHLkxsg1d
93: Eminem - https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR
92: Ed Sheeran - https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V
91: Lil Wayne - https://open.spotify.com/artist/55Aa2cqylxrFIXC767Z865
91: Imagine Dragons - https://open.spotify.com/artist/53XhwfbYqKCa1cC15pYq2q
90: Rihanna - https://open.spotify.com/artist/5pKCCKE2ajJHZ9KAiaK11H
90: Bruno Mars - https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C
89: Ty Dolla $ign - https://open.spotify.com/artist/7c0XG5cIJTrrAgEC3ULPiq
89: Beyoncé - https://open.spotify.com/artist/6vWDO969PvNqNYHIOW5v0m
89: The Chainsmokers - https://open.spotify.com/artist/69GGBxA162lTqCwzJG5jLp
89: Taylor Swift - https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02
89: Maroon 5 - https://open.spotify.com/artist/04gDigrS5kc9YWfZHwBETP
88: Coldplay - https://open.spotify.com/artist/4gzpq5DPGxSnKTe4SA8HAU
88: Panic! At The Disco - https://open.spotify.com/artist/20JZFwl6HVl6yg8a4H3ZqK
88: Twenty One Pilots - https://open.spotify.com/artist/3YQKmKGau1PzlVlkL1iodx
88: The Beatles - https://open.spotify.com/artist/3WrFJ7ztbogyGnTHbHJFl2
87: Wiz Khalifa - https://open.spotify.com/artist/137W8MRPWKqSmrBGDBFSop
87: Logic - https://open.spotify.com/artist/4xRYI6VqpkE3UwrDrAZL8L
87: John Mayer - https://open.spotify.com/artist/0hEurMDQu99nJRq8pTxO14
86: Red Hot Chili Peppers - https://open.spotify.com/artist/0L8ExT028jH3ddEcZwqJJ5

Least popular artists in your library:
7: Zero Mostel & Ronald Holgate - https://open.spotify.com/artist/3RgvYOyVEu9GvHCvt8Bw8j
7: Peter Thom - https://open.spotify.com/artist/3QafxkNr5QQ29cHRhgVsBO
6: Zero Mostel & Brian Davies - https://open.spotify.com/artist/5kAA1r6EEc10lyt3P6PV9A
6: Zero Mostel, Brian Davies & Preshy Marker - https://open.spotify.com/artist/0twdbaZ7R6aJJTX2lqQZfQ
6: Preshy Marker - https://open.spotify.com/artist/5su8grLtxVbtluwIpYxE1W
6: Kelly Markgraf - https://open.spotify.com/artist/1nnoqiJk68QpV6UkvW567W
5: Cowboy '86 - https://open.spotify.com/artist/12F42suF1DlpxJTHPQ88Mc
5: David Burns & Brian Davies - https://open.spotify.com/artist/21ogGr3Hswd9DGqUksGpAf
5: Ronald Holgate & Zero Mostel - https://open.spotify.com/artist/4BwaUNWaZYgWFFt62y44O2
4: Zero Mostel & Jack Gilford - https://open.spotify.com/artist/1TnQrKaNz9N4rpVzWnHZlc
4: Joseph C. Garland - https://open.spotify.com/artist/6xqfWJppseREFAdTDJZ3Tl
4: Julia Bullock - https://open.spotify.com/artist/4hpewChG7FAL2dYXLZUO44
4: Sweet Colleens - https://open.spotify.com/artist/0CszLVIpyMJywvqyM2vXmM
3: Army Field Band - https://open.spotify.com/artist/6DGnfD9vev4wMu5RLRFiU1
2: Ben Markley Big Band - https://open.spotify.com/artist/24k5kQfbeHbcM42vrLcNM2
2: The Guild of Ancient Fifes - https://open.spotify.com/artist/1pWbvZ52zDUckJyfkRwzof
1: Household Division Corps Of Drums & Fifes - https://open.spotify.com/artist/0C9id2SstcR26HDdCVv8hN
1: Matt Wessel - https://open.spotify.com/artist/0Aw5hwpBV9ciBk4LPmpyEa
0: Life Guards Band - https://open.spotify.com/artist/7cGKHORVXtcziLIHUDQQRu
0: Blane, R. - https://open.spotify.com/artist/22yB8AlZgND4xXaJzjyBVg

Most followed artists in your library:
42,948,667: Ed Sheeran - https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V
31,190,930: Rihanna - https://open.spotify.com/artist/5pKCCKE2ajJHZ9KAiaK11H
26,060,720: Eminem - https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR
20,689,526: Bruno Mars - https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C
19,257,177: Taylor Swift - https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02
19,120,277: Coldplay - https://open.spotify.com/artist/4gzpq5DPGxSnKTe4SA8HAU
18,284,766: Beyoncé - https://open.spotify.com/artist/6vWDO969PvNqNYHIOW5v0m
18,093,252: Imagine Dragons - https://open.spotify.com/artist/53XhwfbYqKCa1cC15pYq2q
17,556,383: Maroon 5 - https://open.spotify.com/artist/04gDigrS5kc9YWfZHwBETP
15,188,052: Adele - https://open.spotify.com/artist/4dpARuHxo51G3z768sgnrY
15,128,167: Queen - https://open.spotify.com/artist/1dfeR4HaWDbWqFHLkxsg1d
13,416,117: Demi Lovato - https://open.spotify.com/artist/6S2OmqARrzebs0tKUEyXyp
12,564,556: Twenty One Pilots - https://open.spotify.com/artist/3YQKmKGau1PzlVlkL1iodx
12,128,313: Linkin Park - https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz
11,818,568: The Chainsmokers - https://open.spotify.com/artist/69GGBxA162lTqCwzJG5jLp
11,704,864: Guns N' Roses - https://open.spotify.com/artist/3qm84nBOXUEQ2vnTfUTTFC
11,662,585: The Beatles - https://open.spotify.com/artist/3WrFJ7ztbogyGnTHbHJFl2
10,841,439: AC/DC - https://open.spotify.com/artist/711MCceyCBcFnzjGY4Q7Un
10,228,216: Red Hot Chili Peppers - https://open.spotify.com/artist/0L8ExT028jH3ddEcZwqJJ5
10,201,056: Metallica - https://open.spotify.com/artist/2ye2Wgw4gimLv2eAKyk1NB

Least followed artists in your library:
6: David Burns & Brian Davies - https://open.spotify.com/artist/21ogGr3Hswd9DGqUksGpAf
6: Joanne Miya - https://open.spotify.com/artist/4hqBCPgHlmR9l7pZQmO8Cn
5: Lorin Levee - https://open.spotify.com/artist/601TQkqiAnt3LXTkiR5DnL
5: The Tommy Rome Orchestra - https://open.spotify.com/artist/6wYENXHgHbrqgSaa2qvTDK
5: Cassie Simone - https://open.spotify.com/artist/6FrepzlCnu2TFnlANfjLzh
4: Joseph C. Garland - https://open.spotify.com/artist/6xqfWJppseREFAdTDJZ3Tl
3: Life Guards Band - https://open.spotify.com/artist/7cGKHORVXtcziLIHUDQQRu
3: Louise Marie Cornillez - https://open.spotify.com/artist/4Nd2RJK1wlmkuY4AA36a44
3: Peter Thom - https://open.spotify.com/artist/3QafxkNr5QQ29cHRhgVsBO
2: Household Division Corps Of Drums & Fifes - https://open.spotify.com/artist/0C9id2SstcR26HDdCVv8hN
2: Justin Keyes - https://open.spotify.com/artist/6CEqoRmBXE2VLEhv7aWAWv
1: Eliot Feld - https://open.spotify.com/artist/5IMjTY2XnY6zVAcAyRNp2m
1: Kevin Vortmann - https://open.spotify.com/artist/0caATCnsAyN9vajLJHwDWp
1: Kelly Markgraf - https://open.spotify.com/artist/1nnoqiJk68QpV6UkvW567W
0: John Gower - https://open.spotify.com/artist/125IS9ax8Svaf2rYC1zKoB
0: Blane, R. - https://open.spotify.com/artist/22yB8AlZgND4xXaJzjyBVg
0: Zachary Ford - https://open.spotify.com/artist/4unnkTfw2XrX90l7Cyox14
0: Chris Meissner - https://open.spotify.com/artist/4p2DeTKBXwaNE6A91ahBYA
0: Louis Pardo - https://open.spotify.com/artist/3KfWtx7BKyfaiGQPqDdqAr
0: David Michael Laffey - https://open.spotify.com/artist/5slswoBe6miyP5XNhpWDv9
```