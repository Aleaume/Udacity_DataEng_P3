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

![image](https://user-images.githubusercontent.com/32632731/144011845-560f9c2f-95b4-467f-9364-1f2332668a0f.png)


#### The S3 Bucket

#### The Data Warehouse

#### config script

#### "SQL" files

#### "Execution" scripts

#### Jupyter Notebooks


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

![image](https://user-images.githubusercontent.com/32632731/143939822-4e0d12a6-717a-442a-8051-ccd67a38d08e.png)

## Improvement suggestions / Additional work

