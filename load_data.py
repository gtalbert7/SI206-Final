import sqlite3
import requests
from bs4 import BeautifulSoup

response = requests.get('https://top40weekly.com/top-100-artists-of-the-10s/')
webpage_content = response.text
soup = BeautifulSoup(webpage_content, 'html.parser')

artists_table = soup.find('table')
rows = artists_table.find_all('tr')[1:]  # Skip the header row
artist_names = [row.find_all('td')[2].get_text(strip=True) for row in rows]

conn = sqlite3.connect('artists.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('SELECT COUNT(*) FROM artists')
number_of_artists_already_added = cursor.fetchone()[0]
batch_size = 25
start_index = number_of_artists_already_added
end_index = start_index + batch_size
next_batch = artist_names[start_index:end_index]

for artist in next_batch:
    cursor.execute('INSERT INTO artists (name) VALUES (?)', (artist,))

conn.commit()

cursor.execute('SELECT * FROM artists')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
