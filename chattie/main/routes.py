from chattie.models import Room
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user


main = Blueprint('main', __name__)
clients = []


@main.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    rooms = Room.query.all()
    global clients
    
    return render_template('home.html', 
                           title='home', 
                           rooms=rooms,
                           clients=clients)
