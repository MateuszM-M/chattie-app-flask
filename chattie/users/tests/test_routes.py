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