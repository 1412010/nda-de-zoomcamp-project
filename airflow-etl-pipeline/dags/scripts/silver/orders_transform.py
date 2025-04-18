from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from argparse import ArgumentParser


def transform_orders(input, output):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("OrderTransformation") \
        .getOrCreate()

    # Read raw data from GCS (Bronze layer)
    # input_path = f"gs://{GCP_BUCKET}/bronze/orders*.parquet"
    df = spark.read.parquet(input)
    

    # Silver layer transformation: Clean data
    # silver_df = df \
    #     .filter(col("sale_id").isNotNull() & col("amount").isNotNull()) \
    #     .withColumn("amount", col("amount").cast("float")) \
    #     .withColumn("sale_date", col("sale_date").cast("timestamp"))

    # Write transformed data to GCS (Silver layer)
    # output_path = f"gs://{GCP_BUCKET}/silver/orders.parquet"
    
    df.write.mode("overwrite").parquet(output)

    # Stop Spark session
    spark.stop()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    
    args = parser.parse_args()
    
    transform_orders(args.input, args.output)
