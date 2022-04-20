import os


AWS_ACCESS_KEY_ID = 'V3SPDEOY6JJHHXHQ5XMD'
AWS_SECRET_ACCESS_KEY = 'yJS/xKtoTFbFRwPRyGB55Hk2wsOaPXVAR0jq66cmwfo'
AWS_STORAGE_BUCKET_NAME = 'crowd-predictive-analytics'

AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "https://crowd-predictive-analytics.nyc3.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = "crowdpredictiveanalytics.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "crowdpredictiveanalytics.cdn.backends.StaticRootS3Boto3Storage"
