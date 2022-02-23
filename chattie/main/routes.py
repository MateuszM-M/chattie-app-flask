from chattie.models import Room
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

main = Blueprint('main', __name__)
# clients is a global list of connected, logged in clients 
clients = []


@main.route("/")
def home():
    """
    Returns main page. If not authenticated returns login page.
    Passes rooms and list of clients to template.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    rooms = Room.query.all()
    global clients
    
    return render_template('home.html', 
                           title='home', 
                           rooms=rooms,
                           clients=clients)
