from chattie.models import Message
from chattie import db


def create_message(msg, room, username=None):
    if msg != "":
        message = Message(
            username=username,
            roomname=room,
            message=msg)
        db.session.add(message)
        db.session.commit()
    return {'username': message.username,
            'message': message.message}


def listify(instrumented_list):
    new_list = []
    for user in instrumented_list:
        new_list.append(user.username)
    return new_list