# backend/app/storage.py
import boto3, os, aiofiles
from botocore.config import Config
from typing import Optional

class S3Client:
    def __init__(self):
        self.bucket = os.getenv("S3_BUCKET", "mvp-cmmc-dev")
        self.s3 = boto3.client("s3", config=Config(signature_version='s3v4'))

    async def upload_stream(self, key: str, data: bytes, metadata: Optional[dict]=None):
        # For async usage we just call boto sync in a threadpool; simplified here
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=data, Metadata=metadata or {})
        return f"s3://{self.bucket}/{key}"

    def download_to_file(self, key: str, dest_path: str):
        self.s3.download_file(self.bucket, key, dest_path)
        return dest_path
