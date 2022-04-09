import pytest
from flask import template_rendered
from pytest_factoryboy import register

from chattie import create_app
from chattie.factories import (MessageFactory, ProfileFactory, RoomFactory,
                               UserFactory, SecondUserFactory)
from chattie.models import *

register(UserFactory)
register(SecondUserFactory)
register(ProfileFactory)
register(RoomFactory)
register(MessageFactory)


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })


    ctx = app.test_request_context()
    ctx.push()
    db.create_all()

    yield app

    db.session.commit()
    db.drop_all()
    ctx.pop()

    
@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self.client = client

    def login(self, email, password):
        return self.client.post(
            '/login',
            data={'email': email, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self.client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def user1(app, user_factory):
    """
    Fixture for creating user1 related to profile1, message1
    and room1
    """
    user = user_factory.create()
    return user


@pytest.fixture
def user2(app, second_user_factory):
    user = second_user_factory.create()
    return user


@pytest.fixture
def profile1(profile_factory, user1):
    profile = profile_factory.create(
        id=user1.id,
        user_id=user1.id)
    return profile


@pytest.fixture
def room1(room_factory, user1):
    room = room_factory.create(
        creator_id=user1.id
    )
    return room


@pytest.fixture
def message1(message_factory, user1, room1):
    message = message_factory.create(
        username=user1.username,
        roomname=room1.name
    )
    return message


