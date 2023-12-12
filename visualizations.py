import sqlite3
import matplotlib.pyplot as plt

db_path = 'artists.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = """
    SELECT g.genre, COUNT(*) as count 
    FROM artists a
    JOIN genres g ON a.genre_id = g.id 
    GROUP BY g.genre
"""
cursor.execute(query)
genre_data = cursor.fetchall()

genres_dict = {'Pop': 0, 'Hip Hop/Rap': 0, 'Dance': 0, 'Soul': 0, 'R&B': 0, 'Country': 0, 'Rock': 0, 'Other': 0}
for genre, count in genre_data:
    if 'pop' in genre and 'rap' not in genre:
        genres_dict['Pop'] += count
    elif 'hip hop' in genre or 'rap' in genre:
        genres_dict['Hip Hop/Rap'] += count
    elif 'dance' in genre:
        genres_dict['Dance'] += count
    elif 'soul' in genre:
        genres_dict['Soul'] += count
    elif 'r&b' in genre:
        genres_dict['R&B'] += count
    elif 'country' in genre:
        genres_dict['Country'] += count
    elif 'rock' in genre:
        genres_dict['Rock'] += count
    else:
        genres_dict['Other'] += count

def output_genres_to_file():
    with open('genre_counts.txt', 'w') as f:
        for genre, count in genres_dict.items():
            f.write(f"{genre}: {count}\n")

output_genres_to_file()

genres = list(genres_dict.keys())
counts = list(genres_dict.values())

# chart 1
plt.figure(figsize=(12, 8))
plt.bar(genres, counts, color='skyblue')
plt.xlabel('Genres')
plt.ylabel('Number of Appearances in Top Artists List')
plt.title('Genre Distribution for Top 100 Artists of the 2010s')
plt.show()


query = "SELECT track_name, weeks_on_hot_100 FROM tracks WHERE weeks_on_hot_100 > 0 ORDER BY weeks_on_hot_100 DESC"
cursor.execute(query)
chart_data = cursor.fetchall()

songs = [data[0] for data in chart_data]
weeks_on_chart = [data[1] for data in chart_data]
print(weeks_on_chart)

# chart 2
plt.figure(figsize=(15, 9))
plt.bar(songs, weeks_on_chart, color='teal')
plt.xlabel('Song Names')
plt.ylabel('Weeks on Billboard Hot 100')
plt.title('Current Songs on the Billboard Hot 100 and their Longevity in Weeks')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


query = """
    SELECT g.genre, COUNT(*) as count
    FROM tracks AS t
    JOIN artists AS a ON t.artist_id = a.artist_id
    JOIN genres AS g ON a.genre_id = g.id
    WHERE t.weeks_on_hot_100 > 0
    GROUP BY g.genre
    ORDER BY count DESC
    LIMIT 10
"""
cursor.execute(query)
genre_data = cursor.fetchall()

conn.close()

genres_3 = [data[0] if data[0] else "unknown" for data in genre_data]
counts_3 = [data[1] for data in genre_data]

# chart 3
plt.figure(figsize=(10, 8))
plt.pie(counts_3, labels=genres_3, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Genre Frequency of Top Artists of the 2010s with Current Songs on Billboard Hot 100')
plt.show()

# extra credit visualization
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Genre Distribution for Top 100 Artists of the 2010s')
plt.show()