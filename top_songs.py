import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '84c99acc62714269b6ff371dc4e7dc97'
client_secret = 'b28f081661b64fb592a3c63994614f65'

def get_artists_without_tracks(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, spotify_id FROM artists 
        WHERE id NOT IN (SELECT DISTINCT id FROM tracks)
        ORDER BY id LIMIT 12
    ''')
    return cursor.fetchall()

def add_top_tracks_to_db(conn, spotify):
    artists = get_artists_without_tracks(conn)
    cursor = conn.cursor()
    for artist_id, artist_name, spotify_id in artists:
        top_tracks = spotify.artist_top_tracks(spotify_id, country='US')['tracks'][:2]
        for index, track in enumerate(top_tracks, start=1):
            track_id = f"{artist_id}.{index}"
            track_name = track['name']
            cursor.execute('''
                INSERT INTO tracks (id, name, track_id, track_name) 
                VALUES (?, ?, ?, ?)
            ''', (artist_id, artist_name, track_id, track_name))
    conn.commit()

def main():
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER, name TEXT, track_id TEXT, track_name TEXT,
            FOREIGN KEY (id) REFERENCES artists (id)
        )
    ''')
    conn.commit()
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    add_top_tracks_to_db(conn, spotify)
    conn.close()

main()