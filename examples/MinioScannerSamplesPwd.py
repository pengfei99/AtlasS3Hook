#! /usr/bin/python

from atlaspyapi.client import Atlas
from atlas_s3_hook.S3MetadataClient import S3MetadataClient
from atlas_s3_hook.S3Scanner import S3Scanner
import logging
import os

# config for minio client
minio_end_point = 'changeMe'
minio_access_key = 'changeMe'
minio_secret_key = 'changeMe'
minio_token = "changeMe"

# create an instance of the s3MetadataClient
minio_client = S3MetadataClient(minio_end_point, minio_access_key, minio_secret_key, s3_token=minio_token)

username = "changeMe"
password = "changeMe"

# config for atlas client
atlas_hostname = "https://atlas.lab.sspcloud.fr"
atlas_port = 443
oidc_token = "changeMe"

# create an instance of the Atlas client with login and pwd
atlas_client = Atlas(atlas_hostname, atlas_port, username=username, password=password)

# create an instance of the atlas s3 hook
minio_hook = S3Scanner(minio_client, atlas_client, owner="atlas")

