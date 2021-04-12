from botocore.exceptions import ClientError
from utils import S3URI, S3_URL_PREFIX, ENV, BUCKET_NAME

import boto3
import logging
import os

## acces key, access id = test, test pour que ca fonctionne


def create_bucket(bucket_name=BUCKET_NAME, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket

    try:
        if region is None:
            s3_client = boto3.client('s3', endpoint_url=S3_URL_PREFIX[ENV])
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region, endpoint_url=S3_URL_PREFIX[ENV])
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_bucket_list():

    s3_client = boto3.client('s3', endpoint_url=S3_URL_PREFIX[ENV])
    response = s3_client.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

    return True


def upload_file(file_name, bucket=BUCKET_NAME, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name.split("\\")[-1]
        object_name = object_name.strip()
    else:
        object_name = object_name + ".wav"

    # Upload the file
    s3_client = boto3.client('s3', endpoint_url=S3_URL_PREFIX[ENV])
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_object_list_in_bucket(bucket_name=BUCKET_NAME, s3=None):

    """Get a list of keys in an S3 bucket."""
    keys = []
    resp = s3.list_objects_v2(Bucket=bucket_name)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


def list_obj_bucket(bucket_name=BUCKET_NAME, env=ENV):

    """Get a list of keys in an S3 bucket."""
    s3 = boto3.client('s3', endpoint_url=S3_URL_PREFIX[ENV])
    keys = []
    resp = s3.list_objects_v2(Bucket=bucket_name)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


def download_all_from_s3(bucketName=BUCKET_NAME, path_music='', env=ENV):
    s3 = boto3.client('s3', endpoint_url=S3_URL_PREFIX[ENV])
    my_files = get_object_list_in_bucket(bucketName, s3)
    if not os.path.exists(path_music):
        os.makedirs(path_music)
    try:
        for file in my_files:
            s3.download_file(bucketName, file, path_music + "\\" + file)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def dict_music_from_s3(bucket_name=BUCKET_NAME, env=ENV):
    ### Does not work on AWS S3 bucket because of acces key ID only configured for localstack ###
    audios = {}
    for music in list_obj_bucket(bucket_name):
        # S3 URI ENCODING CORRESPONDING
        for spec_charac in S3URI.keys():
            url_suffix = music.replace(spec_charac, S3URI[spec_charac])
        file = music.split("\\")[-1]
        artist, title_wav = file.split("-")
        artist = artist.strip()
        title = title_wav.split(".")[0].strip()
        elt = {"name": title, "file": S3_URL_PREFIX[env] + url_suffix, "artist": artist, "howl": None}
        #print(S3_URL_PREFIX[ENV] + url_suffix)
        audios.update(elt)
    return audios


if __name__ == "__main__":

    # to do after each localstack server reboot
    # create_bucket(BUCKET_NAME)
    # get_bucket_list()
    # upload_file("D:\\Creations\\69 - Peaches Project\\Jeison - Peaches.wav", bucket=BUCKET_NAME, object_name='Jeison - Peaches')

    #songs = download_all_from_s3(bucketName=BUCKET_NAME, path_music='music', env=ENV)

    #my_files = list_obj_bucket(bucket_name=BUCKET_NAME, env=ENV)
    # print(my_files)

    #download_all_from_s3(bucket_name=BUCKET_NAME, path_music="music")
    #print("ok")

    dict = dict_music_from_s3(bucket_name=BUCKET_NAME, env=ENV)
    print(dict)
