S3URI = {
    " ": "+"
}

BUCKET_NAME = 'test-jeiffer-projet'

DEFAULT_REGION = 'eu-west-3'

S3_URL_PREFIX = {
    'PROD': 'https://' + BUCKET_NAME + '.s3.' + DEFAULT_REGION + '.amazonaws.com/',
    'DEV': 'http://localhost:4566/'
}

WEB_URL_PREFIX = {
    'PROD': 'https://' + BUCKET_NAME + '.s3.' + DEFAULT_REGION + '.amazonaws.com/',
    'DEV': 'http://localhost:5000/'
}

ENV = 'DEV'