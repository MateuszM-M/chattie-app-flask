import pytest
from chattie import bcrypt
from chattie.users.forms import (ChangePasswordForm, RegistrationForm,
                                 RequestResetForm)
from flask_login import login_user


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
    

def test_validate_taken_email(app, user1):
    form = RegistrationForm(data={
        'username': 'username',
        'email': user1.email,
        'password': 'SomePass1!',
        'confirm_password': 'SomePass1!'
    })
    assert form.validate() == False
    assert form.errors == {'email':
        ['That email is taken. Please choose a different one.']}
    

def test_valid_old_password(app, user1):
    login_user(user1)
    form = ChangePasswordForm(data={
        'old_password': 'User1Pass!',
        'new_password': 'SomePass1!NEW',
        'confirm_password': 'SomePass1!NEW'
    })
    assert form.validate() == True
    

def test_invalid_old_password(app, user1):
    login_user(user1)
    form = ChangePasswordForm(data={
        'old_password': 'User1Pass!Incorrect',
        'new_password': 'SomePass1!NEW',
        'confirm_password': 'SomePass1!NEW'
    })
    assert form.validate() == False
    assert form.errors == {'old_password':
        ['Incorrect old password.']}


def test_validate_valid_email(app, user1):
    form = RequestResetForm(
        data={
            'email': user1.email
        })
    assert form.validate() == True
    

def test_validate_valid_email(app):
    form = RequestResetForm(
        data={
            'email': 'incorrect@email.com'
        })
    assert form.validate() == False
    assert form.errors == {'email':
        ['There is no account with that email. You must register first.']}