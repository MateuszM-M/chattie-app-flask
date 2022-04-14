import os
import pathlib

import flask_s3
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_s3 import FlaskS3
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from chattie.config.dev import DevConfig
from chattie.config.local_db import LocalConfig
from chattie.config.prod import ProdConfig

socketio = SocketIO()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
env_path = pathlib.Path(__file__).parent.resolve() / 'config/.env'
load_dotenv(dotenv_path=env_path)
config = os.environ.get("FLASK_CONFIG_MODULE")
s3 = FlaskS3()
mail = Mail()


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    socketio.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    if config == 'chattie.config.prod.ProdConfig':
        s3.init_app(app)
    
    from chattie.chats.routes import chats
    from chattie.main.routes import main
    from chattie.users.routes import users

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(chats)
    
    return app
