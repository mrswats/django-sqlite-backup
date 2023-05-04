import boto3

from testing.constants import TEST_BUCKET_NAME


def get_test_bucket():
    s3 = boto3.client("s3")
    return s3.list_objects(Bucket=TEST_BUCKET_NAME)
