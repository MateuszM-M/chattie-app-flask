import pytest
from chattie.chats.forms import CreateRoomForm


def test_validate_available_room_name(app):
    form = CreateRoomForm(data={
        'name': "game_of_thrones_fans",
    })
    assert form.validate() == True
    assert form.errors == {}


def test_validate_taken_room_name(app, room1):
    form = CreateRoomForm(data={
        'name': room1.name,
    })
    assert form.validate() == False
    assert form.errors == {'name':
        ['That name is taken. Please choose a different one.']}