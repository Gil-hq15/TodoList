import pytest
from app.models import User, Todo
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from flask import url_for, session

@pytest.mark.integration
def test_user_authentication_flow(client):
    """
        Test user authentication workflow, including registration and login.

        This function verifies the user authentication flow:
        - User registration with valid credentials.
        - Login functionality for the newly registered user.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - A user is successfully registered, and a redirect to the login page occurs.
            - The registered user exists in the database.
            - The user can log in successfully, with a redirect to the index page.
    """
    # Test user registration
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password',
        'password1': 'password'
    })
    assert response.status_code == 302  # Redirect to login

    # Verify user in database
    user = User.query.filter_by(username='newuser').first()
    assert user is not None

    # Test login
    response = client.post('/', data={
        'username': 'newuser',
        'password': 'password'
    })
    assert response.status_code == 302  # Redirect to index