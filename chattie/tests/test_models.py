import pytest

from ..models import (Message, Profile, Room, TimestampMixin, User,
                      user_identifier)


def test_user_repr(user1):
    assert user1.__repr__() == f"User('{user1.username}','{user1.email}')"
    
def test_profile_repr(profile1):
    assert profile1.__repr__() == \
    f"Profile('{profile1.id}','{profile1.first_name}', '{profile1.last_name}')"
    
def test_room_repr(room1):
    assert room1.__repr__() == room1.name
    
def test_message_repr(message1):
    assert message1.__repr__() == f"('{message1.username}': '{message1.message[40:]}')"
