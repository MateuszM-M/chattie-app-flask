import pytest
from chattie.users.forms import RegistrationForm


def test_validate_available_username_and_email(app):
    form = RegistrationForm(data={
        'username': "mynameisslimshady",
        'email': 'example@example.com',
        'password': 'SomePass1!',
        'confirm_password': 'SomePass1!'
    })
    assert form.validate() == True
    assert form.errors == {}


def test_validate_taken_username(app, user1):
    form = RegistrationForm(data={
        'username': user1.username,
        'email': 'example@example.com',
        'password': 'SomePass1!',
        'confirm_password': 'SomePass1!'
    })
    assert form.validate() == False
    assert form.errors == {'username':
        ['That username is taken. Please choose a different one.']}
    

def test_validate_taken_username(app, user1):
    form = RegistrationForm(data={
        'username': 'username',
        'email': user1.email,
        'password': 'SomePass1!',
        'confirm_password': 'SomePass1!'
    })
    assert form.validate() == False
    assert form.errors == {'email':
        ['That email is taken. Please choose a different one.']}