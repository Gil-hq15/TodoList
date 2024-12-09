import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Todo, User
from flask import url_for, session


def test_login(client):
    # Create a user
    user = User(username='testuser')
    user.set_password(password='password')
    db.session.add(user)
    db.session.commit()

    # Attempt to log in
    response = client.post('/', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 302  # Check for successful redirect

    # Check session state
    with client.session_transaction() as session:
        assert session.get('user_id') == user.id  # Verify session contains user_id


def test_login_validation(client):
    # Case 1: Missing username
    response = client.post('/', data={'username': '', 'password': 'password'})
    assert response.status_code == 200  # No redirect, show error

    # Case 2: Missing password
    response = client.post('/', data={'username': 'testuser', 'password': ''})
    assert response.status_code == 200  # No redirect, show error

    # Case 3: Both fields empty
    response = client.post('/', data={'username': '', 'password': ''})
    assert response.status_code == 200  # No redirect, show error