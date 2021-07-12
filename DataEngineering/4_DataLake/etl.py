import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

import sys

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('aws', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('aws', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    """ Create spark session """

    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    """
    Fetch song data from S3, processes it and extract song and artist tables from it.
    Convert the data frames to parquet files and loaded back to S3 as output_data.
        
    Parameters:
        spark       : Spark Session
        input_data  : Input json files location in S3 bucket
        output_data : Parquet format stored in S3

    """

    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)
    df.printSchema()

    # extract columns to create songs table    
    songs_table = df.select(df.song_id, df.title, df.artist_id, df.year, df.duration).dropDuplicates()
    
    # write songs table to parquet files partitioned by year and artist
    #songs_table = songs_table.write.partitionBy("year", "artist_id").parquet("/songs.parquet")
    songs_table = songs_table.write.partitionBy("year", "artist_id").mode('overwrite').parquet("/songs.parquet")
    
    # extract columns to create artists table
    artists_table = df.select(df.artist_id, df.artist_name, df.artist_location, df.artist_latitude, df.artist_longitude).dropDuplicates()
    
    # write artists table to parquet files
    artists_table = artists_table.write.mode('overwrite').parquet("/artists.parquet")


def process_log_data(spark, input_data, output_data):
    """
    Fetch log data from S3, processes it and extract users_table, time_table and songplays_tables from it.
    Convert the data frames to parquet files and loaded back to S3 as output_data.
        
    Parameters:
        spark       : Spark Session
        input_data  : Input json files location in S3 bucket
        output_data : Parquet format stored in S3

    """

    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    actions_df = df.filter(df.page == 'NextSong')
    actions_df.printSchema()

    # extract columns for users table    
    users_table = actions_df.select(actions_df.userId, actions_df.firstName, actions_df.lastName, actions_df.gender, actions_df.level).dropDuplicates()
    
    # write users table to parquet files
    users_table = users_table.write.mode('overwrite').parquet("/users.parquet")

    # # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x : str(int(int(x)/1000)))
    actions_df = actions_df.withColumn("timestamp", get_timestamp(actions_df.ts))
    print("creating timestamp column...")
    actions_df.printSchema()
    
    # # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000)))
    actions_df = actions_df.withColumn("datetime", get_datetime(actions_df.ts))
    print("creating datetime column...")
    actions_df.printSchema()
    
    # extract columns to create time table
    time_table = actions_df.select(col('datetime').alias('start_time'), 
                           hour(col('datetime')).alias('hour'),
                           dayofmonth(col('datetime')).alias('day'),
                           weekofyear(col('datetime')).alias('week'),
                           month(col('datetime')).alias('month'),
                           year(col('datetime')).alias('year'),
                           date_format(col('datetime'), "u").alias('weekday')
                          ).dropDuplicates()
    
    print("creating time_table...")
    time_table.printSchema()
    
    # write time table to parquet files partitioned by year and month
    time_table = time_table.write.partitionBy("year", "month").mode('overwrite').parquet("/time_table.parquet")

    # read in song data to use for songplays table
    song_data = input_data + 'song_data/*/*/*/*.json'
    song_df = spark.read.json(song_data)
    
    # extract columns from joined song and log datasets to create songplays table 
    complete_df = song_df.join(actions_df, song_df.title == actions_df.song, "inner" )
    songplays_table = complete_df.select(
                        col('datetime').alias('start_time'),
                        col('userId').alias('userId'),
                        col('level').alias('level'),
                        col('song_id').alias('songId'),
                        col('artist_id').alias('artistId'),
                        col('sessionId').alias('sessionId'),
                        col('location').alias('location'),
                        col('userAgent').alias('user_agent'),
                        year(col('datetime')).alias('year'),
                        month(col('datetime')).alias('month'),
                    ).withColumn('songplay_id', monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    songplays_table = songplays_table.write.partitionBy("year", "month").mode('overwrite').parquet("/songplays_table.parquet")


def main():
    """
    Main method to call process_song_data() and process_log_data() methods.
    """

    spark = create_spark_session()
    input_data = "s3://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
