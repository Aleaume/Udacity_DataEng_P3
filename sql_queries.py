import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP table IF EXISTS staging_events"
staging_songs_table_drop = "DROP table IF EXISTS staging_songs"
songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(\
                                artist varchar,
                                auth varchar,
                                firstname varchar,
                                gender varchar,
                                item_in_session int,
                                lastname varchar,
                                length float,
                                level varchar,
                                location varchar,
                                method varchar,
                                page varchar,
                                registration float,
                                session_id int,
                                song varchar,
                                status int,
                                timestamp timestamp,
                                user_agent varchar,
                                user_id int
    )

""")

staging_songs_table_create = ("""
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(\
                        songplay_id SERIAL PRIMARY KEY, \
                        start_time bigint NOT NULL, \
                        user_id int NOT NULL,\
                        level varchar,\
                        song_id varchar,\
                        artist_id varchar,\
                        session_id int,\
                        location varchar,\
                        user_agent varchar);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(\
                    user_id int PRIMARY KEY,\
                    first_name varchar,\
                    last_name varchar,\
                    gender varchar,\
                    level varchar);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(\
                    song_id varchar PRIMARY KEY,\
                    title varchar,\
                    artist_id varchar NOT NULL,\
                    year int,\
                    duration float);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(\
                        artist_id varchar PRIMARY KEY,\
                        name varchar,\
                        location varchar,\
                        latitude float,\
                        longitude float);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (\
                    start_time bigint PRIMARY KEY,\
                    hour int,\
                    day int,\
                    week int,\
                    month int,\
                    year int,\
                    weekday varchar);
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events from 's3://udacity-dend/log_data/{}' 
credentials 'aws_iam_role={}'
json region 'us-west-2';
""").format('2018/11/2018-11-12-events.json', DWH_ROLE_ARN)


staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays(start_time, user_id,level, song_id, artist_id, session_id, location, user_agent)\
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        
""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level)\
                    VALUES (%s, %s, %s, %s, %s) \
                    ON CONFLICT (user_id) \
                    DO UPDATE SET \
                    level = EXCLUDED.level,\
                    last_name = EXCLUDED.level,\
                    gender = EXCLUDED.gender;
""")

song_table_insert = ("""INSERT INTO songs(song_id, title, artist_id, year, duration)\
                    VALUES (%s, %s, %s, %s, %s) \
                    ON CONFLICT (song_id) \
                    DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists(artist_id, name, location, latitude, longitude)\
                        VALUES (%s, %s, %s, %s, %s) \
                        ON CONFLICT (artist_id) \
                        DO UPDATE SET \
                        name = EXCLUDED.name,\
                        location = EXCLUDED.location, \
                        latitude = EXCLUDED.latitude,\
                        longitude = EXCLUDED.longitude;
""")


time_table_insert = ("""INSERT INTO time(start_time, hour, day, week, month, year, weekday)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s) \
                    ON CONFLICT (start_time) \
                    DO NOTHING;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
