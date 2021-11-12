#! /usr/bin/python

from atlas_client.client import Atlas
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

# config for atlas client
atlas_prod_hostname = "https://atlas.lab.sspcloud.fr"
atlas_prod_port = 443
oidc_token = "changeMe"

# create an instance of the atlas Client with oidc token
atlas_prod_client = Atlas(atlas_prod_hostname, atlas_prod_port, oidc_token=oidc_token)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

minio_hook = S3Scanner(minio_client, atlas_prod_client, owner="atlas")

# upload the metadata of a s3 bucket to atlas, not including the content's metadata of the bucket
minio_hook.add_bucket("pengfei")

# upload the metadata of a s3 directory to atlas, not including the content's metadata (e.g. object) of the directory
minio_hook.add_dir("changeMe", description="add some description")

# upload the metadata of a s3 object to atlas
minio_hook.add_object("changeMe", description="add some description")

# upload the metadata of a path and all its contents to Atlas
path = "donnees-insee"
minio_hook.scan_path(path)
