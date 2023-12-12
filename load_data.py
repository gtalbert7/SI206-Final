import sqlite3
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        spotify_id TEXT NOT NULL UNIQUE,
        genre TEXT
    )
    ''')

    cursor.execute('SELECT COUNT(*) FROM artists')
    number_of_artists_already_added = cursor.fetchone()[0]
    batch_size = 25
    start_index = number_of_artists_already_added
    end_index = start_index + batch_size
    next_batch = artist_names[start_index:end_index]

    for artist in next_batch:
        result = sp.search(q='artist:' + artist, type='artist')
        items = result['artists']['items']
        if items:
            spotify_id = items[0]['id']
            genres = items[0]['genres']
            genre = genres[0] if genres else "Unknown"
            cursor.execute('INSERT OR IGNORE INTO artists (name, spotify_id, genre) VALUES (?, ?, ?)', (artist, spotify_id, genre))
        else:
            cursor.execute('INSERT OR IGNORE INTO artists (name) VALUES (?)', (artist,))
    conn.commit()

    cursor.execute('SELECT * FROM artists')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

load_data()