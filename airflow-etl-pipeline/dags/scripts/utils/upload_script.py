from google.cloud import storage
import logging

def upload_file_to_gcs(bucket_name, local_path, destination_path):
    """
    Uploads a file to a GCS bucket.
    
    Args:
        bucket_name (str): GCS bucket name.
        local_path (str): Path to the local file.
        destination_path (str): Path to upload inside the bucket.
    """
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_path)
        
        blob.upload_from_filename(local_path)
        # with open(local_path, "rb") as f:
        #     blob.upload_from_file(f)
    except Exception as err:
        logging.warning(f"⚠️ ERROR: {err}")
    finally:
        logging.info(f"✅ Uploaded {local_path} to gs://{bucket_name}/{destination_path}")
    