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
    #spotipy_redirect_url='https://localhost:8888/callback'
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
        spotify_id TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('SELECT COUNT(*) FROM artists')
    number_of_artists_already_added = cursor.fetchone()[0]
    batch_size = 25
    start_index = number_of_artists_already_added
    end_index = start_index + batch_size
    next_batch = artist_names[start_index:end_index]

    #i = 0
    for artist in next_batch:
    #    i += 1
        result = sp.search(q='artist:' + artist, type='artist')
        items = result['artists']['items']
        spotify_id = items[0]['id'] if items else None
        cursor.execute('INSERT OR IGNORE INTO artists (name, spotify_id) VALUES (?, ?)', (artist, spotify_id))
    #print(i)
    conn.commit()

    cursor.execute('SELECT * FROM artists')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

load_data()