import os


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'crowd-predictive-analytics'

AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = f"https://{AWS_STORAGE_BUCKET_NAME}.nyc3.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = "crowdpredictiveanalytics.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "crowdpredictiveanalytics.cdn.backends.StaticRootS3Boto3Storage"
