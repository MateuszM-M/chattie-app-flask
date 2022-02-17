from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_socketio import send, emit, join_room, leave_room

from chattie import app, bcrypt, db, socketio
from chattie.forms import (CreateRoomForm, LoginForm,
                           RegistrationForm)

from .models import Message, Room, User, user_identifier


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', login_form=login_form)


clients = []

@app.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    rooms = Room.query.all()
    global clients
    
    return render_template('home.html', 
                           title='home', 
                           rooms=rooms,
                           clients=clients)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/edit-profile")
def edit_profile():
    return "<h1>Page for editing profile</h1>"


@app.route("/change-password")
def change_password():
    return "<h1>Change password page</h1>"


@app.route("/reset-password")
def reset_password():
    return "<h1>reset password </h1>"


@app.route("/create-room", methods=['GET', 'POST'])
@login_required
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        room = Room(name=form.name.data, creator_id=current_user.id)
        db.session.add(room)
        db.session.commit()
        flash(f"Your room:{room.name} has been created!", 'success')
        return redirect(url_for('home'))    
    return render_template('create_room.html', title='Create_room', form=form)


@app.route("/r/<room_name>", methods=['GET', 'POST'])
@login_required
def room(room_name):
    room = Room.query.filter_by(name=room_name).first()
    messages = Message.query.filter_by(room=room)
    users = room.participants
    return render_template('room.html', 
                           title=room.name,
                           room=room,
                           messages=messages,
                           users=users)
    
    
@socketio.on('connect')
def handle_connect():
    try:
        username = current_user.username
        global clients
        if not username in clients:
            clients.append(username)
        emit('userlist_update', clients, broadcast=True)
    except AttributeError:
        pass
       

@socketio.on('disconnect')
def handle_disconnect():
    try:
        username = current_user.username
        global clients
        clients.remove(username)
        emit('userlist_update', clients, broadcast=True)
    except ValueError:
        pass


def create_message(msg, room, username=None):
    if msg != "":
        message = Message(
            username=username,
            roomname=room,
            message=msg)
        db.session.add(message)
        db.session.commit()
    return {'username': message.username, 'message': message.message}


@socketio.on('message')
def handle_message(msg, room, username=None):
    message = create_message(msg, room, username)
    send(message, broadcast=True, to=room)
    
    
def listify(instrumented_list):
    new_list = []
    for user in instrumented_list:
        new_list.append(user.username)
    return new_list
        
        
@socketio.on('join_room')
def handle_join(data):
    username = data['username']
    roomname = data['room']
    user_obj = User.query.filter_by(username=username).first()
    room_obj = Room.query.filter_by(name=roomname).first()
    room_clients = room_obj.participants
    
    join_room(roomname)
    
    if user_obj not in room_clients:
        
        
        statement = user_identifier.insert().values(room_name=roomname,
                                                    user_username=username)
        db.session.execute(statement)
        db.session.commit()
    
        message = f"{username} has entered the room."
        handle_message(message, roomname)
        
        
    room_clients = listify(room_clients)
    print(room_clients)
    emit('roomlist_update', room_clients)
    
    
@socketio.on('leave_room')    
def handle_leave(data):
    username = data['username']
    roomname = data['room']
    room_obj = Room.query.filter_by(name=roomname).first()
    user_obj = User.query.filter_by(username=username).first()
    room_clients = room_obj.participants

    
    if user_obj in room_clients:
    
        leave_room(roomname)
        
        message = f"{username} has left the room."
        handle_message(message, roomname)
        print(room_clients)
        room_clients.remove(user_obj)
        db.session.commit()
        print('removed')
        print(room_clients)
    
    room_clients = listify(room_clients)
    emit('roomlist_update', room_clients)


@app.route("/update/<room_name>", methods=['GET', 'POST'])
@login_required
def update_room(room_name):

    room = Room.query.filter_by(name=room_name).first()
    
    if request.method == 'POST':
        if room.creator_id != current_user.id:
            abort(403)
    
    form = CreateRoomForm()
    if form.validate_on_submit():
        room.name = form.name.data
        db.session.commit()
        flash(f"Your room:{room.name} has been updated!", 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = room.name
    return render_template('create_room.html', title='Update_room', form=form)


@app.route("/delete/<room_name>", methods=['GET', 'POST'])
@login_required
def delete_room(room_name):
    
    room = Room.query.filter_by(name=room_name).first()
    
    if request.method == 'POST':
        if room.creator_id != current_user.id:
            abort(403)
        db.session.delete(room)
        db.session.commit()
        flash(f"{room.name} has been deleted!", 'success')
        return redirect(url_for('home'))
    
    
    return render_template('delete_room.html', title=f"delete {room.name}", room=room)
