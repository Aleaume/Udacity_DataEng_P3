# Udacity_DataEng_P3
Udacity Course, Data Engineering Nanodegree, 2nd Project, Data Warehouse with Amazon Redshift

## Requirements

The following modules need to be installed:

- psycopg2
- boto3
- ipython-sql

Make sure the file dwh.cfg is filled in with AWS section (key, secret, session_token).


## Overview

In this project the goal is to design & create the appropriate Data Warehouse on AWS Redshift with its tables for a music streaming app (sparkify)
Once done, the task is to set up and execute an ETL pipeline capable of 2 major steps:
The first step is to fetch the data stored in a publicly available S3 bucket and store it in staging tables.
And the second is populate previously designed star Schema (https://github.com/Aleaume/Udacity_DataEng_P1) with this data.


### Architecture

The project is composed of different cloud components and a few scripts working together as described in this diagram:

![image](https://user-images.githubusercontent.com/32632731/144019507-0df97b95-04b6-4cfb-b016-1e84cdaee1df.png)


#### The S3 Bucket

An AWS Bucket made publicly available, own & managed by udacity.
s3://udacity-dend/
It contains the different dataset needed for this project, that will be picked up by the etl.py scripts and copied over into the Redshift instance.
For more details on the dataset see the section "Dataset" = > https://github.com/Aleaume/Udacity_DataEng_P3#dataset 

#### The Data Warehouse

The Data warehouse used in this exercise is an AWS Redshift cluser. It is actually configured and set up via jupyter notebook (see section below).
In this example we made used of the following parameters:

Param | Value 
--- | --- 
DWH_CLUSTER_TYPE	| multi-node
DWH_NUM_NODES	| 4
DWH_NODE_TYPE	| dc2.large
DWH_CLUSTER_IDENTIFIER	| dwhCluster
	
#### Config file

The dwh.cfg file is mainly used for setting up the Redhsift instance but is also called at each DB query to authentify and get the right Database.
There are 4 sections:
- Cluster, for all Redhshift & DB parameters
- IAM Role
- S3
- AWS

#### "SQL" file

The sql_queries.py file is the main placeholder for SQL queries exectued in this project. There are calls by either the etl.py , the create_tables.py or the test jupyter notebook.

There are mainly grouped into 4 groups:
- Table creation
- Copy ingestion
- Star schema tables inserts
- Testing

#### "Execution" scripts

There are 2 main execution scripts in this project.
- create_tables.py focused on creatin both the staging tables & the star schema tables (more details in the section Tables Creation & queries)
- etl.py used for the pickup of the data from S3 (Extract), the copy in the staging tables and the insert in a more suitable format in final tables (Transform & Load)

#### Jupyter Notebooks

There are 2 (optional) Jupyer Notebooks in this project:
- redshift_create.ipynb which main role is to create the redhsift cluster, create the needed policy & role to access an S3 bucker, and opening the TCP port to communicate to the cluster. Also, this notebook can be used to decommisioned everything created.
- test.ipynb a simple notebook to test that the ETL task went well.

### Dataset

#### Song Data

- The song dataset is coming from the Million Song Dataset (https://labrosa.ee.columbia.edu/millionsong/). 
Each file contains metadat about 1 song and is in json format. 
Folder structure goes as follow: song_data/[A-Z]/[A-Z]/[A-Z]/name.json 

Here is an example of the file structure:

```json

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, 
"artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", 
"title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

```

- The Song data S3 bucket endpoint is : s3://udacity-dend/song_data

#### Log Data

- The second dataset is generated from an event simulator (https://github.com/Interana/eventsim) based on songs in the previous dataset. Also in json it containes the logs of activity of the music streaming app.
Folder structure goes as follow : log_data/[year]/[month]/[year]-[month]-[day]-events.json
The file structure itself is similar to this:

![image](https://user-images.githubusercontent.com/32632731/141263859-72aa801e-bad3-4a23-86e4-7898c3cca585.png)

- The Song data S3 bucket endpoint is : s3://udacity-dend/log_data and the json path: s3://udacity-dend/log_json_path.json

## Tables Creation & queries

- The staging tables are simply design as complete replicas of the structure of the json files and goes as described here:

![image](https://user-images.githubusercontent.com/32632731/143940527-05d48049-afcd-4e62-affb-46b28bab4e2f.png)

### staging_events

```SQL
CREATE TABLE IF NOT EXISTS staging_events(\
                                artist varchar,
                                auth varchar,
                                firstName varchar,
                                gender varchar,
                                itemInSession int,
                                lastName varchar,
                                length float,
                                level varchar,
                                location varchar,
                                method varchar,
                                page varchar,
                                registration float,
                                sessionId int,
                                song varchar,
                                status int,
                                ts bigint,
                                userAgent varchar,
                                userId int
    )

```

### staging_songs

```SQL

CREATE TABLE IF NOT EXISTS staging_songs(\
                                num_songs int,
                                artist_id varchar,
                                artist_latitude float,
                                artist_longitude float,
                                artist_location varchar,
                                artist_name varchar,
                                song_id varchar,
                                title varchar,
                                duration float,
                                year int

    )

```


- The sparkify DB and tables is created as showed in this diagramm, following Star Schema, were the songplays table is the fact table and the other 4 (users, songs, artists, time) are the dimension tables:

![image](https://user-images.githubusercontent.com/32632731/142909873-78d3c213-c4b4-4b67-a788-6fc1814a15f8.png)



### songplays

```SQL

CREATE TABLE IF NOT EXISTS songplays(\
                        songplay_id int IDENTITY(0,1) PRIMARY KEY, \
                        start_time timestamp NOT NULL, \
                        user_id int NOT NULL,\
                        level varchar,\
                        song_id varchar,\
                        artist_id varchar,\
                        session_id int,\
                        location varchar,\
                        user_agent varchar);

```

### users

```SQL
CREATE TABLE IF NOT EXISTS users(\
                    user_id int PRIMARY KEY,\
                    first_name varchar,\
                    last_name varchar,\
                    gender varchar,\
                    level varchar);

```

### songs

```SQL
CREATE TABLE IF NOT EXISTS songs(\
                    song_id varchar PRIMARY KEY,\
                    title varchar,\
                    artist_id varchar NOT NULL,\
                    year int,\
                    duration float);

```

### artists

```SQL

CREATE TABLE IF NOT EXISTS artists(\
                        artist_id varchar PRIMARY KEY,\
                        name varchar,\
                        location varchar,\
                        latitude float,\
                        longitude float);

```

### time

```SQL
CREATE TABLE IF NOT EXISTS time (\
                    start_time timestamp PRIMARY KEY,\
                    hour int,\
                    day int,\
                    week int,\
                    month int,\
                    year int,\
                    weekday int);

```



## Redshift

## ETL (Extract Transform Load)

Composed of two major steps, the copy of the data from the S3 bucket to the staging tables & the insert into the final tables:

### COPY into Staging tables

#### staging_events

```SQL
("""
	copy staging_events from 's3://udacity-dend/log_data/' 
	credentials 'aws_iam_role={}'
	format json as 's3://udacity-dend/log_json_path.json'
	region 'us-west-2'
	dateformat 'auto';
""").format(ARN)

```
#### staging_songs

```SQL

("""
	copy staging_songs from 's3://udacity-dend/song_data/{}' 
	credentials 'aws_iam_role={}'
	format as json 'auto'
	region 'us-west-2';
""").format('',ARN)

```

### INSERTS into final tables

#### songplays

```SQL
INSERT INTO songplays(start_time, user_id,level, song_id, artist_id, session_id, location, user_agent)\
                                SELECT DISTINCT timestamp 'epoch' + CAST(e.ts AS BIGINT)/1000 * interval '1 second' ,\
                                        e.userId, e.level, s.song_id, s.artist_id, e.sessionId, e.location, e.userAgent \
                                FROM staging_events e \
                                INNER JOIN staging_songs s \
                                ON e.song = s.title AND \
                                e.artist = s.artist_name AND \
                                e.length = s.duration \
                                WHERE e.page = 'NextSong' \
                                AND userID IS NOT NULL;

```

#### users

```SQL
INSERT INTO users(user_id, first_name, last_name, gender, level)\
                            SELECT DISTINCT userId, firstName, lastName, gender, level \
                            FROM staging_events \
                            WHERE page = 'NextSong'\
                            AND userID IS NOT NULL;

```

#### songs

```SQL
INSERT INTO songs(song_id, title, artist_id, year, duration)\
                            SELECT DISTINCT song_id, title, artist_id, year, duration \
                            FROM staging_songs;

```

#### artists

```SQL

INSERT INTO artists(artist_id, name, location, latitude, longitude)\
                            SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude \
                            FROM staging_songs;
```

#### time

```SQL
INSERT INTO time(start_time, hour, day, week, month, year, weekday)\
                            SELECT DISTINCT timestamp 'epoch' + CAST(ts AS BIGINT)/1000 * interval '1 second' AS ts_ts, \
                            EXTRACT(HOUR FROM ts_ts), \
                            EXTRACT(DAY FROM ts_ts), \
                            EXTRACT(WEEK FROM ts_ts),\
                            EXTRACT(MONTH FROM ts_ts),\
                            EXTRACT(YEAR FROM ts_ts), \
                            EXTRACT(WEEKDAY FROM ts_ts)  \
                            FROM staging_events \
                            WHERE page = 'NextSong';

```

### Execution

All is called at once from the etl.py file and we can see in Redshift the execution results & times

![image](https://user-images.githubusercontent.com/32632731/143939822-4e0d12a6-717a-442a-8051-ccd67a38d08e.png)

## Improvement suggestions / Additional work

