from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import os


# Default arguments for the DAG
default_args = {
    "owner": "data_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

GCP_BUCKET = os.environ["GCP_BUCKET"]
GCP_PROJECT_ID = os.environ["GCP_PROJECT"]
GCP_REGION = os.environ["GCP_REGION"]

BQ_DATASET = os.environ["BQ_DATASET"]

# upload_file_to_gcs = scripts.utils.upload_script.upload_file_to_gcs

with DAG(
    "load_to_bq",
    description="Pipeline to load table into Bigquery",
    default_args=default_args,
    params={
        "source_object": "",  # default value
        "bq_table": "",  # default value
    },
    start_date=datetime(2025, 4, 13),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    # Dummy start task
    start = DummyOperator(task_id='start')

    load_to_bq = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket=GCP_BUCKET,
        source_objects=["{{ params.source_object }}"],  # relative to bucket
        destination_project_dataset_table=BQ_DATASET + ".{{ params.bq_table }}",
        source_format="PARQUET",
        write_disposition="WRITE_TRUNCATE",  # or WRITE_APPEND
        autodetect=True,
        location=GCP_REGION,
    )
    
    # Dummy end task
    end = DummyOperator(task_id='end')

    start >> load_to_bq >> end
