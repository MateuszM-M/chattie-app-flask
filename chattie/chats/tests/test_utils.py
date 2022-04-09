import pytest
from chattie import db
from chattie.chats.utils import create_message, listify
from chattie.models import Message, user_identifier


def test_create_message(app, user1, room1):
    msg = create_message(
        msg='Hello world',
        room=room1.name,
        username=user1.username,
    )
    assert len(Message.query.all()) == 1
    assert msg == {'username': user1.username, 'message': 'Hello world'}
   
    
def test_listify(app, user1, user2, room1):
    users = [user1, user2]
    
    for user in users:
        statement = user_identifier.insert().values(
            room_name=room1.name,
            user_username=user.username)
        db.session.execute(statement)
        db.session.commit()
        
    room_clients = listify(room1.participants)
    assert room_clients == [user1.username, user2.username]
    assert room1.participants == [user1, user2]