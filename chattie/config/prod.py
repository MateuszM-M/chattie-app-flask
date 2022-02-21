import os
from .base import *
import flask_s3


class ProdConfig(BaseConfig):
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    SECRET_KEY = os.environ.get("PROD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_SQLALCHEMY_DATABASE_URI")
    FLASKS3_BUCKET_NAME = os.environ.get("S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.environ.get("S3_KEY")
    AWS_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
    FLASKS3_REGION = "eu-central-1"
    