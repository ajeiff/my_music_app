import json
import boto3

from utils import S3URI, S3_URL_PREFIX, ENV

S3URI = {
    " ": "+"
}


def lambda_handler():
    ### Missing arg for aws Lambda: event, context ###
    # TODO implement
    region = 'eu-west-3'
    bucket_name_source = 'test-jeiffer-projet'
    s3 = boto3.client('s3', endpoint_url=S3_URL_PREFIX[ENV])
    dict_songs = {}
    resp = s3.list_objects_v2(Bucket=bucket_name_source)
    for obj in resp['Contents']:
        artist, title = obj['Key'].split("-")
        artist = artist.strip()
        title = title.split(".")[0].strip()
        #payload = s3.get_object(Bucket=bucket_name_source, Key=obj['Key'])["Body"]
        url_suffix = obj['Key']
        for spec_charac in S3URI.keys():
            url_suffix = url_suffix.replace(spec_charac, S3URI[spec_charac])
        url_obj = 'https://' + bucket_name_source + '.s3.' + region + '.amazonaws.com/' + url_suffix
        elt = {"name": title, "file": url_obj, "artist": artist, "howl": None}
        dict_songs.update(elt)

    return {
        'statusCode': 200,
        'body': json.dumps(dict_songs)
    }