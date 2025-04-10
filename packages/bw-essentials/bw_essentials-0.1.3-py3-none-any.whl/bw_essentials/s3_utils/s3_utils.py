"""
Module for interacting with AWS S3.

This module contains a class, S3Utils, which facilitates operations
like uploading, downloading, listing, and deleting files in an AWS S3 bucket.
"""
import logging
from typing import Optional, List

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class S3Utils:
    """
    S3Utils class for managing S3 operations.
    """

    def __init__(self, access_key, secret_key):
        """
        Initialize the S3Utils with AWS configuration.
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3_instance = self._get_s3_instance()

    def _get_s3_instance(self):
        """
        Returns an S3 client instance.
        """
        try:
            return boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
        except Exception as exp:
            logger.error("Error getting S3 client", exc_info=exp)
            raise

    def download_file(self, bucket_name: str, file_key: str, local_path: str):
        try:
            if not file_key or not local_path:
                raise ValueError("file_key and local_path are required.")
            self.s3_instance.download_file(bucket_name, file_key, local_path)
            logger.info(f"File downloaded from {bucket_name}/{file_key} to {local_path}")
        except Exception as e:
            logger.error("Error downloading file", exc_info=e)
            raise

    def upload_file(self, bucket_name: str, path_to_file: str, object_name: str, content_type: str):
        logger.info(f"Uploading file: {path_to_file} to {bucket_name}/{object_name}")
        try:
            with open(path_to_file, 'rb') as file_object:
                self.s3_instance.put_object(
                    Bucket=bucket_name,
                    Key=object_name,
                    Body=file_object,
                    ContentType=content_type
                )
            logger.info("Upload successful")
        except Exception as e:
            logger.error("Error uploading file", exc_info=e)
            raise

    def list_files(self, bucket_name: str, prefix: Optional[str] = "") -> List[str]:
        try:
            response = self.s3_instance.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            files = [item['Key'] for item in response.get('Contents', [])]
            logger.info(f"Found {len(files)} files in {bucket_name}/{prefix}")
            return files
        except Exception as e:
            logger.error("Error listing files", exc_info=e)
            raise

    def delete_file(self, bucket_name: str, file_key: str):
        try:
            self.s3_instance.delete_object(Bucket=bucket_name, Key=file_key)
            logger.info(f"Deleted {file_key} from {bucket_name}")
        except Exception as e:
            logger.error("Error deleting file", exc_info=e)
            raise

    def delete_files_by_prefix(self, bucket_name: str, prefix: str):
        try:
            objects = self.list_files(bucket_name, prefix)
            if not objects:
                logger.info("No files to delete.")
                return
            delete_payload = {'Objects': [{'Key': key} for key in objects]}
            self.s3_instance.delete_objects(Bucket=bucket_name, Delete=delete_payload)
            logger.info(f"Deleted {len(objects)} files under prefix {prefix}")
        except Exception as e:
            logger.error("Error deleting files by prefix", exc_info=e)
            raise

    def get_latest_file_by_prefix(self, bucket_name: str, prefix: str) -> Optional[str]:
        try:
            response = self.s3_instance.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            contents = response.get('Contents', [])
            if not contents:
                return None
            latest = max(contents, key=lambda x: x['LastModified'])
            logger.info(f"Latest file under {prefix} is {latest['Key']}")
            return latest['Key']
        except Exception as e:
            logger.error("Error getting latest file by prefix", exc_info=e)
            raise

    def file_exists(self, bucket_name: str, file_key: str) -> bool:
        try:
            self.s3_instance.head_object(Bucket=bucket_name, Key=file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            logger.error("Error checking file existence", exc_info=e)
            raise

    def read_file_content(self, bucket_name: str, file_key: str, encoding="utf-8") -> str:
        try:
            obj = self.s3_instance.get_object(Bucket=bucket_name, Key=file_key)
            content = obj['Body'].read().decode(encoding)
            return content
        except Exception as e:
            logger.error("Error reading file content", exc_info=e)
            raise

    @staticmethod
    def get_object_url(bucket_name: str, object_name: str) -> str:
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
