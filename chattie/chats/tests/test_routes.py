import pytest
from chattie.models import (Message, Profile, Room, TimestampMixin, User,
                     user_identifier)


def test_get_create_room_view(auth, client, user1):
    auth.login(user1.email, 'User1Pass!')
    response = client.get('/create-room')
    assert len(Room.query.all()) == 0
    assert response.status_code == 200
    assert response.request.path == "/create-room"


def test_create_valid_room(auth, client, user1):
    auth.login(user1.email, 'User1Pass!')
    response = client.post('/create-room',
                           data={
                               'name': 'ChamberOfSecrets'
                           },
                           follow_redirects=True)
    assert len(Room.query.all()) == 1
    assert response.status_code == 200
    assert response.request.path == "/"
    

def test_fail_creating_invalid_room(auth, client, user1):
    auth.login(user1.email, 'User1Pass!')
    response = client.post('/create-room',
                           data={
                               'name': ''
                           },
                           follow_redirects=True)
    assert len(Room.query.all()) == 0
    assert response.status_code == 200
    assert response.request.path == "/create-room"
    

def test_get_room_view(auth, client, user1, room1):
    auth.login(user1.email, 'User1Pass!')
    response = client.get(f'/chat?room_name={room1.name}')
    assert response.status_code == 200
    assert response.request.path == '/chat'
    

def test_get_update_room_view(auth, client, user1, room1):
    auth.login(user1.email, 'User1Pass!')
    response = client.get(f'/update/{room1.name}')
    assert response.status_code == 200
    assert response.request.path == f'/update/{room1.name}'


def test_valid_update_room(auth, client, user1, room1):
    auth.login(user1.email, 'User1Pass!')
    response = client.post(f'/update/{room1.name}',
                           data={
                               'name': 'NewName'
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/'
    assert Room.query.filter_by(id=room1.id).first().name == 'NewName'


def test_invalid_update_room(auth, client, user1, room1):
    auth.login(user1.email, 'User1Pass!')
    old_name = room1.name
    response = client.post(f'/update/{room1.name}',
                           data={
                               'name': ''
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == f'/update/{room1.name}'
    assert Room.query.filter_by(id=room1.id).first().name == old_name
    
    
def test_invalid_user_update_room(auth, client, user1, room1, user2):
    auth.login(user2.email, 'User1Pass!')
    old_name = room1.name
    response = client.post(f'/update/{room1.name}',
                           data={
                               'name': 'IncorrectUser'
                           })
    assert Room.query.filter_by(id=room1.id).first().name == old_name
    assert response.request.path == f'/update/{room1.name}'
    
    









def test_get_delete_room_view(auth, client, user1, room1):
    auth.login(user1.email, 'User1Pass!')
    response = client.get(f'/delete/{room1.name}')
    assert response.status_code == 200
    assert response.request.path == f'/delete/{room1.name}'


def test_valid_delete_room(auth, client, user1, room1):
    auth.login(user1.email, 'User1Pass!')
    response = client.post(f'/delete/{room1.name}',
                           follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/'
    assert len(Room.query.all()) == 0

    
def test_invalid_user_delete_room(auth, client, user1, room1, user2):
    auth.login(user2.email, 'User1Pass!')
    response = client.post(f'/delete/{room1.name}')
    assert len(Room.query.all()) == 1
    assert response.request.path == f'/delete/{room1.name}'


    
