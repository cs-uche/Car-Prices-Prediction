#!/usr/bin/env python3

import boto3
import logging
import sys
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """
    Create an S3 bucket in a specified region.
    
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    Parameters:
    - bucket_name: Bucket to create
    - region: String region to create the bucket in, e.g., 'us-west-2'

    Returns:
    - True if the bucket is created, else False
    """
    try:
        s3 = boto3.client('s3', region_name=region) if region else boto3.client('s3')
        
        if region:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        else:
            s3.create_bucket(Bucket=bucket_name)
        
    except ClientError as client_err:
        logging.error(f"Error creating S3 bucket {bucket_name}: {client_err}")
        logging.error("Exit Code: ", client_err.response['ResponseMetadata']['HTTPStatusCode'])
        sys.exit(1)
    
    return 200