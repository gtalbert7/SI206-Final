import sqlite3
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def load_data():
    response = requests.get('https://top40weekly.com/top-100-artists-of-the-10s/')
    webpage_content = response.text
    soup = BeautifulSoup(webpage_content, 'html.parser')
    client_id = '84c99acc62714269b6ff371dc4e7dc97'
    client_secret = 'b28f081661b64fb592a3c63994614f65'
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    artists_table = soup.find('table')
    rows = artists_table.find_all('tr')[1:]  # Skip the header row
    artist_names = [row.find_all('td')[2].get_text(strip=True) for row in rows]

    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artist_ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_id INTEGER NOT NULL,
        spotify_id TEXT UNIQUE,
        genre_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artist_ids(id),
        FOREIGN KEY (genre_id) REFERENCES genres(id)
    )
    ''')

    def get_or_create_genre_id(genre):
        cursor.execute('SELECT id FROM genres WHERE genre = ?', (genre,))
        result = cursor.fetchone()
        if result:
            return result[0]
        cursor.execute('INSERT INTO genres (genre) VALUES (?)', (genre,))
        return cursor.lastrowid

    def get_or_create_artist_id(name):
        cursor.execute('SELECT id FROM artist_ids WHERE name = ?', (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        cursor.execute('INSERT INTO artist_ids (name) VALUES (?)', (name,))
        return cursor.lastrowid

    cursor.execute('SELECT COUNT(*) FROM artist_ids')
    number_of_artists_already_added = cursor.fetchone()[0]
    batch_size = 25
    start_index = number_of_artists_already_added
    end_index = min(start_index + batch_size, len(artist_names))
    next_batch = artist_names[start_index:end_index]

    for artist in next_batch:
        artist_id = get_or_create_artist_id(artist)
        result = sp.search(q='artist:' + artist, type='artist')
        items = result['artists']['items']
        if items:
            spotify_id = items[0]['id']
            genres = items[0]['genres']
            genre_id = get_or_create_genre_id(genres[0] if genres else "unknown")
            cursor.execute('INSERT OR IGNORE INTO artists (artist_id, spotify_id, genre_id) VALUES (?, ?, ?)', (artist_id, spotify_id, genre_id))

    conn.commit()

    cursor.execute('SELECT * FROM artists')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

load_data()
