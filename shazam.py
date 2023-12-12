import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from top_songs import add_top_tracks_to_db



batch_size = 25
api_key = '40333609'

def create_table(): 
    conn = sqlite3.connect('artists.db')  
    cursor = conn.cursor() 

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER,
            name TEXT,
            track_id TEXT,
            track_name TEXT,
            shazam_count INTEGER,  
            FOREIGN KEY (id) REFERENCES artists (id)
        )
    ''')

    conn.commit()
    conn.close()

    
def get_shazam_count(track_name):
  
   
    base_url = "https://shazam.p.rapidapi.com/songs/get-count"
    

    headers = {
        "X-RapidAPI-Key": "658358df4fmshea041f36d27b47fp185941jsnb5ee2134e5e1",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
       
    }

    params = {
        "term": track_name,
        "key": api_key
    }


    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  

        data = response.json()
        shazam_count = data.get("total", 0)

        print(f"Track: {track_name}, Shazam Count: {shazam_count}")

        return shazam_count
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving Shazam count for {track_name}: {e}")
        return None
    


def insert_shazam_count(track_id, track_name, shazam_count): 
    conn = sqlite3.connect('artist.db')  
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tracks (track_id, track_name, shazam_count)
        VALUES (?, ?, ?)
        ON CONFLICT (track_id)  
        DO UPDATE SET shazam_count = ?;
    ''', (track_id, track_name, shazam_count, shazam_count))

    conn.commit()
    conn.close()



def main():
    
    create_table()

    conn = sqlite3.connect('artists.db')  
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='84c99acc62714269b6ff371dc4e7dc97', client_secret='b28f081661b64fb592a3c63994614f65'))

    add_top_tracks_to_db(conn, spotify)
    
    
    cursor = conn.cursor()
    cursor.execute('SELECT track_id, track_name FROM tracks WHERE shazam_count IS NULL LIMIT ?;', (batch_size,))
    tracks = cursor.fetchall()
    conn.close()

    for track_id, track_name in tracks:
        shazam_count = get_shazam_count(track_name)
        if shazam_count is not None:
            insert_shazam_count(track_id, track_name, shazam_count)

if __name__ == "__main__":
    main()




