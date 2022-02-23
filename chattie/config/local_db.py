import os

from .base import *


class LocalConfig(BaseConfig):
    FLASK_ENV = 'local_db'
    FLASK_DEBUG = True
    SECRET_KEY = '3c46ee1eb7ec14e26c429fac7525184531e3d7ef3f514254191ceeabeed2d50c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
