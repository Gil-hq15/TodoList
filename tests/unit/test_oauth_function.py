from unittest.mock import patch
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User


def test_oauth_login(client):
    """
        Test OAuth login functionality with Google OAuth service.

        This function simulates the OAuth login process with Google's OAuth service:
        - Mocks the user information returned by the OAuth service (Google).
        - Patches the functions responsible for authorizing and parsing the OAuth tokens.
        - Simulates the OAuth callback and verifies the user is created in the database.
        - Checks if the user is redirected to the index page and the session contains the correct `user_id`.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The response status is a redirect (302) to the index page.
            - A new user is created in the database with the correct username.
            - The session contains the correct `user_id` after successful login.
            - The user's password is not stored in plain text.
    """
    # Mock user info returned by Google's OAuth service
    mock_user_info = {
        'sub': 'google-unique-id',
        'name': 'Test User',
        'email': 'testuser@example.com'
    }

    # Mock `authorize_access_token` and `parse_id_token`
    with patch('app.oauth.google.authorize_access_token') as mock_authorize, \
         patch('app.oauth.google.parse_id_token') as mock_parse:
        
        mock_authorize.return_value = {'id_token': 'mock_token'}
        mock_parse.return_value = mock_user_info

        # Simulate OAuth callback
        with client.session_transaction() as session:
            session['nonce'] = 'mock_nonce'  # Set nonce to match callback logic

        response = client.get('/oauth-callback')

        # Check redirect to the index page
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/index'

        # Verify user creation in the database
        user = User.query.filter_by(username='Test User').first()
        assert user is not None
        assert user.username == 'Test User'
        assert user.password_hashed != 'oauth'

        # Verify session contains user_id
        with client.session_transaction() as session:
            assert session['user_id'] == user.id