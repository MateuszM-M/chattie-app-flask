import pathlib

from dotenv import load_dotenv

env_path = pathlib.Path(__file__).parent.resolve() / '.env'
load_dotenv(dotenv_path=env_path)


class BaseConfig:
    """
    Base environment configuration. 
    Other configs inherit from here.
    """
    FLASK_APP='run.py'
    