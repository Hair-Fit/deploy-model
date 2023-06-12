from google.cloud import storage
from google.oauth2 import service_account
import os
import asyncio
from urllib.parse import urlparse
storage_client = storage.Client(
    project="august-edge-384214",
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


asyncio.run(download_blob("https://storage.cloud.google.com/tfjs-model-hair-fit/tfjs-test-1.zip"))


