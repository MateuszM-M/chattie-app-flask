import os
from .base import *


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get("DEV_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_SQLALCHEMY_DATABASE_URI")