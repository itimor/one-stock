import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIAQL37NL4YRJPBIUIC'
ACCESS_SECRET_KEY = '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'
region_name = 'ap-east-1'
BUCKET_NAME = 'baicai1'

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    region_name=region_name,
    config=Config(signature_version='s3v4')
)


def put_s():
    data = open('aaa.py', 'rb')
    s3.Bucket(BUCKET_NAME).put_object(Key='aaa.py', Body=data)


def list_s():
    listObjSummary = s3.Bucket(BUCKET_NAME).objects.all()
    for objSum in listObjSummary:
        print('Item:')
        print(objSum.key)


if __name__ == '__main__':
    # list()
    put_s()
    print("Done")
