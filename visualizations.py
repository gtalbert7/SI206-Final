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

print(genres)
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print(counts)

# chart 1
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Genre Distribution in Artists Table')
plt.show()


query = "SELECT track_name, weeks_on_hot_100 FROM tracks WHERE weeks_on_hot_100 > 0 ORDER BY weeks_on_hot_100 DESC"
cursor.execute(query)
chart_data = cursor.fetchall()


songs = [data[0] for data in chart_data]
weeks_on_chart = [data[1] for data in chart_data]

# chart 2
plt.figure(figsize=(15, 10))
plt.bar(songs, weeks_on_chart, color='teal')
plt.xlabel('Songs')
plt.ylabel('Weeks on Billboard Hot 100')
plt.title('Songs and their Weeks on Billboard Hot 100')
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

genres = [data[0] if data[0] else "Unknown" for data in genre_data]
counts = [data[1] for data in genre_data]

# chart 3
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
plt.title('Genre Frequency of Artists with Top Ten Charting Songs on Billboard Hot 100')
plt.show()
