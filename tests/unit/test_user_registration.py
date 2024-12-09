import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Todo, User


def test_user_registration(client):
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
    # Submit registration form with non-matching passwords
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password123',
        'password1': 'password321'
    })
    assert response.status_code == 200  # No redirect, show error


def test_registration_existing_user(client):
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