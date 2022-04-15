import os
import pathlib

from dotenv import load_dotenv


env_path = pathlib.Path(__file__).parent.resolve() / '.env'
load_dotenv(dotenv_path=env_path)


class BaseConfig:
    """
    Base environment configuration. 
    Other configs inherit from here.
    """
    # Base config
    FLASK_APP='run.py'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    # Mail config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
