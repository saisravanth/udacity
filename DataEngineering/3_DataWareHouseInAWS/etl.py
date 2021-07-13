import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Description: This function can be used to execute copy commands in 'copy_table_queries' list i.e copying data from S3 bucket into staging tables available in EC2 instance.

    Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """
    for query in copy_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description: This function is used to execute all queries in 'insert_table_queries' list. Esentially populating fact and dimension tables.

    Arguments:
        cur: the cursor object.
        conn: connection object to AWS Redshift DB.

    Returns:
        None
    """
    for query in insert_table_queries:
        print("query: ", query)
        cur.execute(query)
        conn.commit()

def main():
    """
    Description: This function is used to make connection to AWS Redshift DB using parameters in 'config.cfg'. Then call functions load_staging_tables() and insert_tables() with cursor and connection arguments.

    Arguments:
        None

    Returns:
        None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()