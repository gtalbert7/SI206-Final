import sqlite3
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
#from spotipy.oauth2 import SpotifyOAuth
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

client_id = '84c99acc62714269b6ff371dc4e7dc97'
client_secret = 'b28f081661b64fb592a3c63994614f65'
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def find_artist_id(artist_name):
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="84c99acc62714269b6ff371dc4e7dc97", client_secret="b28f081661b64fb592a3c63994614f65"))

    results = spotify.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        return artist['id']
    else:
        return None

# Example usage
artist_id = find_artist_id("Drake")
if artist_id:
    print("Artist ID for Drake:", artist_id)
else:
    print("Drake not found")

# def get_top_artists_in_usa():
#     # List of top artists in the USA (you need to provide these artist IDs)
#     artist_ids = ['ARTIST_ID_1', 'ARTIST_ID_2', 'ARTIST_ID_3', 'ARTIST_ID_4', 'ARTIST_ID_5']

#     for artist_id in artist_ids:
#         # Get top tracks of the artist in the USA
#         top_tracks = spotify.artist_top_tracks(artist_id, country='US')

#         # Print artist name and top tracks
#         artist = spotify.artist(artist_id)
#         print(f"Top tracks for {artist['name']}:")
#         for track in top_tracks['tracks']:
#             print(f" - {track['name']}")

# # Call the function
# get_top_artists_in_usa()

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
# results = spotify.artist_top_tracks(lz_uri)

# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()

'''
TODO LIST:
1. Collect top 5 artists in specific countries on Spotify
--- https://www.youtube.com/watch?v=kaBVN8uP358&t=0s
- USA
- England
- Brazil
2. Collect top 5 songs from each artist collected, on Spotify
3. Compare those songs to how many times they have been shazamed
- Compare those songs to each other within an artist
- Compare artists to other artists within a country
- Compare countries to each other
4. Compare those songs to different billboard chart placements
'''