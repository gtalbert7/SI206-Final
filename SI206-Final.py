import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])

'''
TODO LIST:
1. Collect top 5 artists in specific countries on Spotify
--- https://www.youtube.com/watch?v=kaBVN8uP358&t=0s
- USA
- Canada
- Mexico
- England
- Brazil
2. Collect top 5 songs from each artist collected, on Spotify
3. Compare those songs to how many times they have been shazamed
- Compare those songs to each other within an artist
- Compare artists to other artists within a country
- Compare countries to each other
4. Compare those songs to different billboard chart placements
'''