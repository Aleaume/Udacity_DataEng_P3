import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    
     """
    Description: This function is responsible for reading the json file in the s3 bucket, and copyting the data in the staging tables
    
    Arguments:
        cur: the cursor object.
        filepath: song data file path.
        
    Returns:
        None
    """
    
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    
    """
    Description: This function is insert data into the final tables from the staging tables.
    
    Arguments:
        cur: the cursor object.
        filepath: song data file path.
        
    Returns:
        None
    """
    
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    
     """
    Description: This function is the main function of this file.
                 It creates the connection to the DB and its cursor.
                 Then calls the respective etl functions to
                 execute the complete etl pipeline.
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
