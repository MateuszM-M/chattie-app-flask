from chattie import db, socketio
from chattie.chats.forms import CreateRoomForm
from chattie.main.routes import clients
from chattie.models import Message, Room, User, user_identifier
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from flask_socketio import emit, join_room, leave_room, send

from .utils import create_message, listify

chats = Blueprint('chats', __name__)


@chats.route("/create-room", methods=['GET', 'POST'])
@login_required
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        room = Room(name=form.name.data, creator_id=current_user.id)
        db.session.add(room)
        db.session.commit()
        flash(f"Your room:{room.name} has been created!", 'success')
        return redirect(url_for('main.home'))    
    return render_template('create_room.html',
                           title='Create_room',
                           form=form)


@chats.route("/chat", methods=['GET', 'POST'])
@login_required
def room():
    room_name = request.args.get('room_name')
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


@socketio.on('message', namespace="/chat")
def handle_message(msg, room, username=None):
    message = create_message(msg, room, username)
    send(message, broadcast=True, to=room)
        
   
@socketio.on('connect', namespace="/chat")
def handle_join():
    username = current_user.username
    # update to allow multi word room names
    roomname = request.referrer.split("=")[1]
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
        
        
    room_clients = listify(room_obj.participants)
    emit('roomlist_update', room_clients, broadcast=True, to=roomname)
    
    
@socketio.on('disconnect', namespace="/chat")
def handle_leave():
    username = current_user.username
    roomname = request.referrer.split("=")[1]
    room_obj = Room.query.filter_by(name=roomname).first()
    user_obj = User.query.filter_by(username=username).first()
    room_clients = room_obj.participants
    
    if user_obj in room_clients:
    
        leave_room(roomname)
        
        message = f"{username} has left the room."
        handle_message(message, roomname)

        room_obj.participants.remove(user_obj)
        db.session.commit()
    
    room_clients = listify(room_obj.participants)
    emit('roomlist_update', room_clients, braadcast=True, to=roomname)


@chats.route("/update/<room_name>", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = room.name
    return render_template('create_room.html',
                           title='Update_room',
                           form=form)


@chats.route("/delete/<room_name>", methods=['GET', 'POST'])
@login_required
def delete_room(room_name):
    
    room = Room.query.filter_by(name=room_name).first()
    
    if request.method == 'POST':
        if room.creator_id != current_user.id:
            abort(403)
        db.session.delete(room)
        db.session.commit()
        flash(f"{room.name} has been deleted!", 'success')
        return redirect(url_for('main.home'))
    
    
    return render_template('delete_room.html',
                           title=f"delete {room.name}",
                           room=room)
    