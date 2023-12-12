import sqlite3
import billboard

def remove_features(track_name):
    if ' (feat.' in track_name:
        return track_name.split(' (feat.')[0].strip()
    elif ' (with' in track_name:
        return track_name.split(' (with')[0].strip()
    elif ' [with' in track_name:
        return track_name.split(' [with')[0].strip()
    else:
        return track_name

def get_weeks_on_chart(song_titles):
    song_weeks = {}
    chart = billboard.ChartData('hot-100')

    for song in chart:
        song_title_cleaned = remove_features(song.title).lower()
        if song_title_cleaned in song_titles:
            index = song_titles.index(song_title_cleaned)
            original_title = song_titles[index]
            song_weeks[original_title] = song.weeks

    return song_weeks

db_path = 'artists.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS update_offset (
        id INTEGER PRIMARY KEY,
        offset INTEGER DEFAULT 0
    )
''')

cursor.execute("SELECT offset FROM update_offset WHERE id = 1")
result = cursor.fetchone()
if result:
    offset = result[0]
else:
    offset = 0
    cursor.execute("INSERT INTO update_offset (id, offset) VALUES (1, 0)")

cursor.execute("SELECT track_id, track_name FROM tracks LIMIT 25 OFFSET ?", (offset,))
batch_tracks = cursor.fetchall()

track_names = [remove_features(track[1]).lower() for track in batch_tracks]
track_id_name_map = {remove_features(track[1]).lower(): track[0] for track in batch_tracks}

weeks_on_chart = get_weeks_on_chart(track_names)

try:
    cursor.execute("ALTER TABLE tracks ADD COLUMN weeks_on_hot_100 INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass

for track_name, weeks in weeks_on_chart.items():
    track_id = track_id_name_map.get(track_name)
    if track_id:
        cursor.execute("UPDATE tracks SET weeks_on_hot_100 = ? WHERE track_id = ?", (weeks, track_id))

new_offset = offset + 25
cursor.execute("UPDATE update_offset SET offset = ? WHERE id = 1", (new_offset,))

conn.commit()
conn.close()

print(f"Updated 'tracks' table with 'weeks_on_hot_100' data for 25 rows starting from offset {offset}.")