import pytest
from chattie.models import *
from chattie import bcrypt
from flask import g, session


def test_get_login_view(client):
      response = client.get("/login")
      assert response.status_code == 200
      assert response.request.path == "/login"


def test_valid_login(client, user1):
      response = client.post('/login',
                              data={'email': user1.email, 
                                    'password': 'User1Pass!'},
                              follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/"
    
    
def test_invalid_login(client):
      response = client.post('/login',
                        data={'email': 'SomeLogin', 
                              'password': 'SomePass123#'},
                        follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/login"
      
      
def test_login_redirect_as_logged_in(auth, client, user1):
      auth.login(user1.email, 'User1Pass!')
      response = client.get('/login', follow_redirects=True)
      assert response.request.path == "/"
      
      
def test_logout(auth, client, user1):
      auth.login(user1.email, 'User1Pass!')
      response = client.get('/logout', follow_redirects=True)
      
      assert response.status_code == 200
      assert response.request.path == "/login"
      
      
def test_register_redirect_as_logged_in(auth, client, user1):
      auth.login(user1.email, 'User1Pass!')
      response = client.get('/register', follow_redirects=True)
      assert response.request.path == "/"
      

def test_get_register_view(client):
      response = client.get("/register")
      assert response.status_code == 200


def test_valid_register(client):
      response = client.post('/register',
                  data={'username': 'Username1',
                        'email': 'Name@example.com', 
                        'password': 'SomePass123#',
                        'confirm_password': 'SomePass123#'},
                  follow_redirects=True)
      assert len(User.query.all()) == 1
      assert response.request.path == "/login"
      

def test_invalid_register(client):
      response = client.post('/register',
                  data={'username': 'Username1',
                        'email': 'Name@example.com', 
                        'password': 'SomePass123#',
                        'confirm_password': 'IncorrectPassword'},
                  follow_redirects=True)
      assert len(User.query.all()) == 0
      assert response.request.path == "/register"
      
      
def test_get_edit_profile_view(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.get("/edit-profile")
      assert response.status_code == 200
      
      
def test_valid_edit_profile(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.post("/edit-profile",
                             data={
                                   'username': user1.username,
                                   'email': user1.email,
                                   'first_name': 'Name',
                                   'last_name': 'Surname',
                                   'country': 'Poland',
                                   'city': 'Warsaw',
                                   'about': "I'll be back"},
                                   follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/"
      assert profile1.first_name == 'Name'
      assert profile1.last_name == 'Surname'
      assert profile1.country == 'Poland'
      assert profile1.city == 'Warsaw'
      assert profile1.about == "I'll be back"
      
      
def test_valid_edit_user(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.post("/edit-profile",
                             data={
                                   'username': 'New_username',
                                   'email': 'mail@example.com'},
                                   follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/"
      assert user1.username == "New_username"
      assert user1.email == "mail@example.com"
      

def test_valid_edit_user_and_profile(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.post("/edit-profile",
                             data={
                                   'username': 'New_username',
                                   'email': 'mail@example.com',
                                   'first_name': 'Name',
                                   'last_name': 'Surname',
                                   'country': 'Poland',
                                   'city': 'Warsaw',
                                   'about': "I'll be back"},
                                   follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/"
      assert user1.username == "New_username"
      assert user1.email == "mail@example.com"
      assert profile1.first_name == 'Name'
      assert profile1.last_name == 'Surname'
      assert profile1.country == 'Poland'
      assert profile1.city == 'Warsaw'
      assert profile1.about == "I'll be back"
      

def test_invalid_edit_user(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      old_name = user1.username
      old_email = user1.email
      response = client.post("/edit-profile",
                             data={
                                   'username': '',
                                   'email': ''},
                                   follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/edit-profile"
      assert user1.username == old_name
      assert user1.email == old_email


def test_get_change_password_view(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.get("/change-password")
      assert response.status_code == 200
      
      
def test_valid_change_password(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.post("/change-password",
                             data={
                                   'old_password': 'User1Pass!',
                                   'new_password': 'User1Pass!NEW',
                                   'confirm_password': 'User1Pass!NEW',
                             },
                             follow_redirects=True)
      assert response.status_code == 200
      assert response.request.path == "/"
      client.get('/logout', follow_redirects=True)
      auth.login(user1.email, 'User1Pass!NEW')
      assert response.status_code == 200
      assert response.request.path == "/"
      
      
def test_invalid_old_password(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.post("/change-password",
                             data={
                                   'old_password': 'User1Pass!INCORRECT',
                                   'new_password': 'User1Pass!NEW',
                                   'confirm_password': 'User1Pass!NEW',
                             },
                             follow_redirects=True)
      assert response.request.path == "/change-password"
      client.get('/logout', follow_redirects=True)
      response = auth.login(user1.email, 'User1Pass!INCORRECT')
      assert response.request.path == "/login"
      response = auth.login(user1.email, 'User1Pass!')
      assert response.request.path == "/"
      

def test_invalid_confirm_password(auth, client, user1, profile1):
      auth.login(user1.email, 'User1Pass!')
      response = client.post("/change-password",
                             data={
                                   'old_password': 'User1Pass!',
                                   'new_password': 'User1Pass!NEW',
                                   'confirm_password': 'User1Pass!INCORRECT',
                             },
                             follow_redirects=True)
      assert response.request.path == "/change-password"
      client.get('/logout', follow_redirects=True)
      response = auth.login(user1.email, 'User1Pass!NEW')
      assert response.request.path == "/login"
      response = auth.login(user1.email, 'User1Pass!INCORRECT')
      assert response.request.path == "/login"
      response = auth.login(user1.email, 'User1Pass!')
      assert response.request.path == "/"