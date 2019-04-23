# Test notes

* To trigger rate limit responses, run `most_popular_for.py "Ennio Morricone":
   there are 600 albums and 9k+ tracks, it should trigger several rate limit events
* "Prince" isn't the most popular artist return for `most_popular_for "Prince"`
   even though it's an exact match - useful to test