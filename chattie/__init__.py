from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = '3c46ee1eb7ec14e26c429fac7525184531e3d7ef3f514254191ceeabeed2d50c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
socketio=SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from chattie import routes
