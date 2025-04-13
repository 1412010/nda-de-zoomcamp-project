import argparse
import os
from time import time
import pandas as pd
from sqlalchemy import create_engine


DB_HOST = "postgres_db"
DB_PORT = "5432"
DB_USER = "root"
DB_PW = "root"
DB_NAME = "instacart"

DATA_FOLDER = "./data"


def load_products_table(engine) -> bool:

    table_name = "products"
    df = pd.read_csv(f'{DATA_FOLDER}/{table_name}.csv')
    
    # Synthesize more columns for data
    
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False) 
    except Exception as e:
        print(f"ERROR: Cannot load table {table_name}!")
        print("Detail: ", e)
        return False
    print("Successfully ingested table products!")

    return True

def load_aisles_table(engine) -> bool:

    table_name = "aisles"
    df = pd.read_csv(f'{DATA_FOLDER}/{table_name}.csv')
    
    # Synthesize more columns for data
    
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False) 
    except Exception as e:
        print(f"ERROR: Cannot load table {table_name}!")
        print("Detail: ", e)
        return False
    print("Successfully ingested table aisles!")
    return True

def load_departments_table(engine) -> bool:

    table_name = "departments"
    df = pd.read_csv(f'{DATA_FOLDER}/{table_name}.csv')
    # Synthesize more columns for data
    
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False) 
    except Exception as e:
        print(f"ERROR: Cannot load table {table_name}!")
        print("Detail: ", e)
        return False
    print("Successfully ingested table departments!")
    return True

def load_orders_table(engine) -> bool:

    table_name = "orders"
    df_iter = pd.read_csv(f'{DATA_FOLDER}/{table_name}.csv', iterator=True, chunksize=100000)
    
    # Synthesize more columns for data
    
    df = next(df_iter)
    # Create table with header only
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    

    while True:
        t_start = time()
        
        try:    
            df = next(df_iter)
            
            # Synthesize more columns
        
            result = df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            total_rows += result
        
        except StopIteration:
            print(f"✅ Loaded {table_name} table succesfully!. Total rows count: {total_rows}")
            return True

        except Exception as e:
            print(f"ERROR: Cannot load table {table_name}!")
            print("Detail: ", e)
            return False
        
        t_end = time()
        print(f'inserted chunk of {result} rows, took {(t_end - t_start):.3f} seconds')

    return True


def load_order_products_prior_table(engine) -> bool:
    csv_name = "order_products__prior"
    table_name = "order_products_prior"
    df_iter = pd.read_csv(f'{DATA_FOLDER}/{csv_name}.csv', iterator=True, chunksize=100000)
    
    # Synthesize more columns for data
    
    df = next(df_iter)
    # Create table with header only
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    
    total_rows = 0

    while True:
        t_start = time()
        
        try:    
            df = next(df_iter)
            
            # Synthesize more columns
        
            result = df.to_sql(name=table_name, con=engine, if_exists='append')
            total_rows += result
        
        except StopIteration:
            print(f"✅ Loaded {table_name} table succesfully!. Total rows count: {total_rows}")

            return True

        except Exception as e:
            print(f"ERROR: Cannot load table {table_name}!")
            print("Detail: ", e)
            return False
        
        t_end = time()
        print(f'inserted chunk of {result} rows, took {(t_end - t_start):.3f} seconds')


def main():    
    # Create engine and connect to Postgres DB
    DB_URL = f'postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DB_URL)
    
    # load_aisles_table(engine)
    load_departments_table(engine)
    # load_products_table(engine)
    # load_orders_table(engine)
    # load_order_products_prior_table(engine)
    
    engine.dispose()
    
    
if __name__ == '__main__':
    main()
    
    
    