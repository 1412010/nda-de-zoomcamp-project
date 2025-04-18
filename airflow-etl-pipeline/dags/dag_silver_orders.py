import sys

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
import os
from scripts.utils.upload_script import upload_file_to_gcs



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

# upload_file_to_gcs = scripts.utils.upload_script.upload_file_to_gcs

with DAG(
    "silver_orders",
    description="Pipeline to transform `orders` table from bronze to silver",
    default_args=default_args,
    params={
        "dataproc_cluster": "",  # default value
    },
    start_date=datetime(2025, 4, 13),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    # Dummy start task
    start = DummyOperator(task_id='start')

    upload_script = PythonOperator(
        task_id="upload_script_to_gcs",
        python_callable=upload_file_to_gcs,
        op_kwargs={
            "bucket_name": GCP_BUCKET,
            "local_path": "/opt/airflow/dags/scripts/silver/orders_transform.py",
            "destination_path": "_scripts/dataproc_job.py"
        }
    )

    # Submit Dataproc job (PySpark)
    dataproc_job = {
        "reference": {"project_id": GCP_PROJECT_ID},
        "placement": {"cluster_name": "{{ params.dataproc_cluster }}"},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{GCP_BUCKET}/_scripts/dataproc_job.py",
            "args": [
                "--input", f"gs://{GCP_BUCKET}/bronze/order_products_prior*.parquet.gzip",
                "--output", f"gs://{GCP_BUCKET}/silver/orders.parquet"
            ],
        },
    }

    run_dataproc = DataprocSubmitJobOperator(
        task_id="run_dataproc_job",
        job=dataproc_job,
        region=GCP_REGION,
        project_id=GCP_PROJECT_ID
    )
    
    # Dummy end task
    end = DummyOperator(task_id='end')

    start >> upload_script >> run_dataproc >> end
