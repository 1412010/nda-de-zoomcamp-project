import pandas as pd
from sqlalchemy import create_engine
from google.cloud import storage
import io
import gc

DB_HOST = "postgres_db"
DB_PORT = "5432"
DB_USER = "root"
DB_PW = "root"
DB_NAME = "instacart"

CHUNK_SIZE = 100000

# GCS config
BUCKET_NAME = "instacart-dev-bucket"
DESTINATION_BLOB_NAME = "bronze"
GCP_KEY_PATH = "gcp_service_acc_key.json"


def create_database_connection():
    # Create engine and connect to Postgres DB
    DB_URL = f'postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DB_URL)
    return engine


def export_chunks_to_parquet_gcs(engine, table_name):
    print(f"Start extracting table {table_name} to GCS...")
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    QUERY = f"SELECT * FROM {table_name}"
    chunk_iter = pd.read_sql_query(QUERY, con=engine, chunksize=CHUNK_SIZE)

    for i, chunk_df in enumerate(chunk_iter):
        try:
            buffer = io.BytesIO()
            chunk_df.to_parquet(buffer, compression='gzip', engine='pyarrow', index=False)
            buffer.seek(0)

            blob_name = f"{DESTINATION_BLOB_NAME}/{table_name}_part-{i:03}.parquet.gzip"
            blob = bucket.blob(blob_name)
            blob.upload_from_file(buffer, content_type="application/octet-stream")
            
            del chunk_df
            del buffer

        except Exception as err:
            print(f"ERROR: Failed to read or upload data of table {table_name} to GCS.")
            return
        
        gc.collect()       

    print(f"✅ All chunks exported to GCS folder: gs://{BUCKET_NAME}/{DESTINATION_BLOB_NAME}/")


def main():
    print("Hello world")
    # Create engine and connect to Postgres DB
    DB_URL = f'postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DB_URL)
    print(engine) 
    if not engine:
        print("Cannot create database connection")
    else:
        for table in [ "order_products_prior"]:  # "products", "aisles", "departments", "orders",
            export_chunks_to_parquet_gcs(engine, table)
    
    engine.dispose()


if __name__ == "__main__":
    main()
