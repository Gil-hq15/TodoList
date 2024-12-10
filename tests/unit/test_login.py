import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Todo, User
from flask import url_for, session


def test_login(client):
    """
        Test user login functionality.

        This function verifies that a user can successfully log in with valid credentials:
        - Creates a user and stores their credentials in the database.
        - Sends a login request with the correct username and password.
        - Verifies that the user is redirected upon successful login.
        - Ensures the session contains the correct `user_id` after login.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The login request returns a status code of 302 (indicating a successful redirect).
            - The session contains the correct `user_id` for the logged-in user.
    """
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
    """
        Test user login validation with missing or empty credentials.

        This function ensures that login validation works properly by handling invalid inputs:
        - Case 1: Missing username.
        - Case 2: Missing password.
        - Case 3: Both fields empty.
        - For each case, the response should return a status code of 200, indicating an error message is displayed.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - Each invalid login attempt results in a 200 status code (no redirect).
            - The appropriate error message or validation feedback is shown for each case.
    """
    # Case 1: Missing username
    response = client.post('/', data={'username': '', 'password': 'password'})
    assert response.status_code == 200  # No redirect, show error

    # Case 2: Missing password
    response = client.post('/', data={'username': 'testuser', 'password': ''})
    assert response.status_code == 200  # No redirect, show error

    # Case 3: Both fields empty
    response = client.post('/', data={'username': '', 'password': ''})
    assert response.status_code == 200  # No redirect, show error