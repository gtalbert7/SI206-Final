import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '84c99acc62714269b6ff371dc4e7dc97'
client_secret = 'b28f081661b64fb592a3c63994614f65'

def get_artists_without_tracks(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT artist_id, spotify_id FROM artists 
        WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM tracks)
        ORDER BY artist_id LIMIT 12
    ''')
    return cursor.fetchall()

def add_top_tracks_to_db(conn, spotify):
    artists = get_artists_without_tracks(conn)
    cursor = conn.cursor()
    for artist_id, spotify_id in artists:
        top_tracks = spotify.artist_top_tracks(spotify_id, country='US')['tracks'][:2]
        for index, track in enumerate(top_tracks, start=1):
            track_id = f"{artist_id}.{index}"
            track_name = track['name']
            cursor.execute('''
                INSERT INTO tracks (artist_id, track_id, track_name) 
                VALUES (?, ?, ?)
            ''', (artist_id, track_id, track_name))
    conn.commit()

def main():
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            artist_id INTEGER, track_id TEXT, track_name TEXT,
            FOREIGN KEY (artist_id) REFERENCES artist_ids (id)
        )
    ''')
    conn.commit()
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    add_top_tracks_to_db(conn, spotify)
    conn.close()

main()
