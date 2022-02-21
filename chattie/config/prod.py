import os
from .base import *


class ProdConfig(BaseConfig):
    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    SECRET_KEY = os.environ.get("PROD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_SQLALCHEMY_DATABASE_URI")