import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
#config.read_file(open('C:\\Users\\sravg\Downloads\\2020 Learning\\Data Engineer Nanodegree\\Projects\\3 Data warehouse in AWS\\dwh.cfg'))

SONG_DATA = config.get('S3', 'SONG_DATA')
ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')

# for section_name in config.sections():
#     print('Section:', section_name)
#     print('Options:', config.options(section_name))
#     for name, value in config.items(section_name):
#         print('%s = %s' % (name, value))


# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
    artist TEXT, 
    auth TEXT,
    firstName VARCHAR(32),
    gender CHAR(1),
    itemInSession INT,
    lastName VARCHAR(32),
    length NUMERIC(7,2),
    level TEXT,
    location TEXT,
    method TEXT,
    page TEXT,
    registration VARCHAR(50), 
    sessionId INT,
    song TEXT,
    status INT, 
    ts TIMESTAMP,
    userAgent TEXT,
    userId INT,
    PRIMARY KEY (ts, sessionId)  
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    num_songs INT IDENTITY(0,1),
    artist_id VARCHAR,
    artist_latitude decimal, 
    artist_longitude decimal,
    artist_location TEXT,
    artist_name VARCHAR(256),
    song_id TEXT PRIMARY KEY,
    title TEXT,
    duration decimal,
    year INT
); 
""")

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id INT IDENTITY(0,1) PRIMARY KEY,
	start_time TIMESTAMP, 
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
    duration decimal
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
    start_time TIMESTAMP PRIMARY KEY, 
    hour INT, 
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday INT
);
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events 
    from {}
    credentials 'aws_iam_role={}'
    json {}
    region 'us-west-2'
    timeformat as 'epochmillisecs';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs 
    from {}
    credentials 'aws_iam_role={}'
    json 'auto'
    region 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays 
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT  
    se.ts as start_time, 
    se.userId, 
    se.level, 
    ss.song_id,
    ss.artist_id, 
    se.sessionId,
    se.location, 
    se.userAgent
FROM staging_events se, staging_songs ss
WHERE se.page = 'NextSong' 
AND se.song = ss.title 
AND se.length = ss.duration;
""")

user_table_insert = ("""
INSERT INTO users 
(user_id, first_name, last_name, gender, level)
SELECT DISTINCT  
    userId, 
    firstName, 
    lastName, 
    gender, 
    level
FROM staging_events
WHERE page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs
(song_id, title, artist_id, year, duration)
SELECT DISTINCT 
    song_id, 
    title,
    artist_id,
    year,
    duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists
(artist_ID, name, location, latitude, longitude)
SELECT DISTINCT 
    artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time 
(start_time, hour, day, week, month, year, weekday)
SELECT start_time, 
    extract(hour from start_time),
    extract(day from start_time),
    extract(week from start_time), 
    extract(month from start_time),
    extract(year from start_time), 
    extract(dayofweek from start_time)
FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
