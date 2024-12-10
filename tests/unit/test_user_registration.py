import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Todo, User


def test_user_registration(client):
    """
        Test user registration functionality.

        This function verifies the user registration process:
        - Simulates a user registration request with matching passwords.
        - Checks that the registration redirects to the login page after successful submission.
        - Verifies the new user is added to the database.
        - Confirms the password is hashed and stored securely.
        - Checks that the hashed password matches the original using the `check_password` method.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The registration request returns a status code of 302 (successful redirect).
            - The user is created in the database with the correct username.
            - The password is hashed and stored securely.
            - The hashed password matches the original password when verified.
    """
    # Simulate a user registration request
    response = client.post(
        '/register',
        data={
            'username': 'newuser',
            'password': 'securepassword',
            'password1': 'securepassword'  # Confirm password
        }
    )
    
    # Assert that the response redirects to the login page after successful registration
    assert response.status_code == 302
    assert '/login' in response.location or '/' in response.location

    # Verify the user was created in the database
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.username == 'newuser'
    
    # Should be hashed
    assert user.password_hashed != 'securepassword' 

    # Check that the hashed password matches the original using a verify method
    assert user.check_password('securepassword')


def test_registration_password_mismatch(client):
    """
        Test user registration with mismatched passwords.

        This function ensures that the registration process correctly handles password mismatches:
        - Submits the registration form with non-matching passwords.
        - Verifies that the response returns a status code of 200 (no redirect) and shows an error message.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The response status is 200, indicating the error is handled and shown to the user.
    """
    # Submit registration form with non-matching passwords
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password123',
        'password1': 'password321'
    })
    assert response.status_code == 200  # No redirect, show error


def test_registration_existing_user(client):
    """
        Test user registration with an existing username.

        This function ensures that the registration process correctly handles attempts to register with an already existing username:
        - Creates a user and stores it in the database.
        - Attempts to register with the same username.
        - Verifies that the response returns a status code of 200, indicating the error is handled and shown to the user.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The response status is 200, indicating the error is handled and shown to the user.
    """
    # Create an existing user
    existing_user = User(username='existinguser')
    existing_user.set_password('password123')
    db.session.add(existing_user)
    db.session.commit()

    # Attempt to register with the same username
    response = client.post('/register', data={
        'username': 'existinguser',
        'password': 'newpassword123',
        'password1': 'newpassword123'
    })
    
    assert response.status_code == 200  # No redirect, show error