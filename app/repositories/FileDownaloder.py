import os
import urllib.request as urlRequest

import boto3
import botocore
import config
from boto3.s3.transfer import S3Transfer


class FileDownaloder:
    currentPath = os.path.dirname(os.path.realpath(__file__))
    parentPath = os.path.abspath(os.path.join(currentPath, os.pardir))
    temp_dir = parentPath + '/Downloads/'

    def __init__(self, url):
        self.url = url
        self.fileName = self.temp_dir + self.download_File()

    def download_File(self):
        # prepare save dir and filename        
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        file_name = self.url.split('/')[-1]
        if "amazon-crawl-data" in self.url:
            self.downloadS3(file_name, self.temp_dir + file_name)
        else:
            try:
                urlRequest.urlretrieve(self.url, self.temp_dir + file_name)
                return file_name
            except Exception as e:
                raise Exception('download error with exception' + str(e))

    def delete_file(self):
        if os.path.exists(self.fileName):
            os.remove(self.fileName)

    def downloadS3(self, file_name, file_name_16_wav):
        credentials = {
            'aws_access_key_id': config.aws_access_key_id,
            'aws_secret_access_key': config.aws_secret_access_key
        }
        s3 = boto3.resource('s3', **credentials)
        BUCKET_NAME = config.BUCKET_NAME
        KEY = config.KEY
        try:
            s3.Bucket(BUCKET_NAME).download_file(KEY + file_name, file_name_16_wav)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return file_name
            else:
                raise

    def upload_To_S3(self, file_name, bucket, key, credentials):
        client = boto3.client('s3', **credentials)
        transfer = S3Transfer(client)
        transfer.upload_file(self.temp_dir + file_name, bucket, key + file_name)
        file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key + file_name)
        return file_url

    def check_if_exists_s3(self, file_name, bucket, key, credentials):
        s3 = boto3.resource('s3', **credentials)
        BUCKET_NAME = bucket
        key = key + file_name
        objs = list(s3.Bucket(BUCKET_NAME).objects.filter(Prefix=key))
        if len(objs) > 0 and objs[0].key == key:
            return True
        else:
            return False
