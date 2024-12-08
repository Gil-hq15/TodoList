import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Todo, User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

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