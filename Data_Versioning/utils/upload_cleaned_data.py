#!/usr/bin/env python3

import boto3
import logging
import os

from datetime import datetime
from botocore.exceptions import ClientError


def upload_cleaned_data(file_name, bucket_name, file_prefix):
    """
    Upload cleaned data to an S3 bucket.

    Parameters:
    - file_name (str): File to upload.
    - bucket_name (str): Bucket to upload to.
    - file_prefix (str): Prefix for the S3 object name.
    """
    
    s3 = boto3.client('s3')
    version = datetime.now().strftime("%Y%m%d")
    object_name = os.path.join("data", "cleaned", version, f'{file_prefix}_v{version}.csv')
    s3_path = f's3://{bucket_name}/{object_name}'
    
    try:
        s3.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        error_message = f"ERROR: Failed to upload {file_name} to {s3_path}"
        print(error_message)
        logging.error(error_message)
    print(f"SUCESS: uploaded to {s3_path}")