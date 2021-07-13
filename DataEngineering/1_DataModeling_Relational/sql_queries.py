# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
	songplay_id SERIAL PRIMARY KEY, 
	start_time BIGINT, 
	user_id TEXT NOT NULL, 
	level TEXT, 
	song_id TEXT, 
	artist_id TEXT, 
	session_id INT NOT NULL, 
	location TEXT, 
	user_agent TEXT
);
""")

user_table_create = ("""
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    first_name VARCHAR(32) NOT NULL, 
    last_name VARCHAR(32) NOT NULL, 
    gender CHAR(1), 
    level TEXT
);
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id TEXT PRIMARY KEY, 
    title TEXT NOT NULL, 
    artist_id TEXT NOT NULL, 
    year INT, 
    duration NUMERIC(5,2)
);

""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id TEXT PRIMARY KEY, 
    name VARCHAR(256) NOT NULL, 
    location TEXT, 
    latitude NUMERIC(7,2), 
    longitude NUMERIC(7,2)
);
""")

time_table_create = ("""
CREATE TABLE time (
    start_time BIGINT, 
    hour INT, 
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday TEXT
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays 
(songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;

""")

user_table_insert = ("""
INSERT INTO users 
(user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs
(song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists
(artist_ID, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""
INSERT INTO time 
(start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_ID 
FROM songs s JOIN artists a
ON s.artist_ID = a.artist_ID
WHERE s.title = %s AND a.name = %s  AND s.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]