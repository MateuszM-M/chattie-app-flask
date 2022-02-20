import os
from .base import *


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get("DEV_SECRET_KEY")