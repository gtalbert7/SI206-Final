import sqlite3
import matplotlib.pyplot as plt

db_path = 'artists.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = "SELECT genre, COUNT(*) as count FROM artists GROUP BY genre"
cursor.execute(query)
genre_data = cursor.fetchall()

genres = [data[0] for data in genre_data]
counts = [data[1] for data in genre_data]

pop = 0
hip_hop_rap = 0
dance = 0
soul = 0
r_b = 0
country = 0
rock = 0
other = 0
for i in range(len(genres)):
    if 'pop' in genres[i] and 'rap' not in genres[i]:
        pop += counts[i]
    elif 'hip hop' in genres[i] or 'rap' in genres[i]:
        if 'pop' not in genres[i]:
            hip_hop_rap += counts[i]
    elif 'dance' in genres[i]:
        dance += counts[i]
    elif 'soul' in genres[i]:
        soul += counts[i]
    elif 'r&b' in genres[i]:
        r_b += counts[i]
    elif 'country' in genres[i]:
        country += counts[i]
    elif 'rock' in genres[i]:
        rock += counts[i]
    else: 
        other += counts[i]
genres = ['Pop', 'Hip Hop/Rap', 'Dance', 'Soul', 'R&B', 'Country', 'Rock', 'Other']
counts = [pop, hip_hop_rap, dance, soul, r_b, country, rock, other]

# print(genres)
# print('~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(counts)

# chart 1
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
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
    SELECT a.genre, COUNT(*) as count
    FROM tracks AS t
    JOIN artists AS a ON t.id = a.id
    WHERE t.weeks_on_hot_100 > 0
    GROUP BY a.genre
    ORDER BY count DESC
    LIMIT 10
"""
cursor.execute(query)
genre_data = cursor.fetchall()

conn.close()

genres_3 = [data[0] if data[0] else "Unknown" for data in genre_data]
counts_3 = [data[1] for data in genre_data]

# chart 3
plt.figure(figsize=(10, 8))
plt.pie(counts_3, labels=genres_3, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Genre Frequency of Top Artists of the 2010s with Current Songs on Billboard Hot 100')
plt.show()

# extra credit visualization
plt.figure(figsize=(12, 8))
plt.bar(genres, counts, color='skyblue')
plt.xlabel('Genres')
plt.ylabel('Number of Appearances in Top Artists List')
plt.title('Genre Distribution for Top 100 Artists of the 2010s')
plt.show()