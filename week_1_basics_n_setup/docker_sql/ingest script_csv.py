#!/usr/bin/env python
# coding: utf-8

import os
import argparse


from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    """Function to ingest data to sql database

    Args:
        param (_type_): _description_
    """
    
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    # engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    # df_p = pd.read_parquet('yellow_tripdata_2024-04.parquet')
    
    while True:
        try:
            t_start = time()
        
            df_p.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace', chunksize=100000)

            t_end = time()

            print('Inserted another chunk, took %.3f second' % (t_end - t_start))
        except StopIteration:
            # StopIteration is raised when the iterator is exhausted
            print('All data processed.')
            break
        except Exception as e:
            # Handle other exceptions
            print(f'An error occurred: {e}')
            # Optionally, you can log the error or take other actions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)