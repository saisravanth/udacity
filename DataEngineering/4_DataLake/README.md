# Data Lake with Apache Spark

# Project Introduction:
A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs that store user activity as well as a directory with JSON metadata on the songs in their app.

The task is to build an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables in spark parquet files. This will allow their analytics team to continue finding insights in what songs their users are listening to.

- Input  - > Json files (s3://udacity-dend/log_data and s3://udacity-dend/song_data)
- Schema - > STAR
- Output - > Parquet format files stored in S3 bucket.  

## Star Schema:
Schema consists of 1 fact table and 4 dimension tables. 

- Fact table: 
    - Table: songplays 
        - Columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
- Dimension tables:
    - Table: users 
        - Columns: user_id, first_name, last_name, gender, level
    - Table: songs
        - Columns: song_id, title, artist_id, year, duration
    - Table: artists
        - Columns: artist_ID, name, location, latitude, longitude
    - Table: time
        - Columns: start_time, hour, day, week, month, year, weekday


# Prerequisites:

- Ensure to setup an EMR cluster (1 parent and n child EC2 instances of any type say m5.xlarge) that is configured with the required IAMRole (S3 Admin access) using either Amazon Console or IAC (Infrastructure as Code using boto3 package in python).

# How To Run:
- If running on EMR cluster:
    - Run etl.py
- If running locally with AWS access:
    - Fill the credentials in dl.cfg
    - Run etl.py

# Files In Repository:
- The project includes three files:
    1. etl.py reads data from S3, processes that data using Spark, and writes them back to S3.
    2. dl.cfg contains AWS credentials (this is optional if running locally without EMR cluster).
    3. README.md 
