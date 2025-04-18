from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from argparse import ArgumentParser

def load_products(input, output):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("ProductLoad") \
        .getOrCreate()

    # Read data from GCS (Silver layer)
    # input_path = f"gs://{GCP_BUCKET}/bronze/products*.parquet"
    df = spark.read.parquet(input)
    
    df.write.mode("overwrite").parquet(output)

    # Stop Spark session
    spark.stop()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    
    args = parser.parse_args()
    
    load_products(args.input, args.output)
