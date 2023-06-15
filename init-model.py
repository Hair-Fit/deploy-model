from google.cloud import storage
from google.oauth2 import service_account
import os
import asyncio
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
storage_client = storage.Client(
    project=os.environ.get('GCP_PROJECT'),
    credentials=service_account.Credentials.from_service_account_file('serviceaccount.json')
)
def decode_gcs_url(url):
    p = urlparse(url)
    path = p.path[1:].split('/', 1)
    bucket, file_path = path[0], path[1] 
    return bucket, file_path

async def download_blob(url):
    if url:
        bucket, file_path = decode_gcs_url(url)
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(file_path)
        blob.download_to_filename(os.path.basename(file_path))


asyncio.run(download_blob(os.environ.get('MODEL_URL')))


