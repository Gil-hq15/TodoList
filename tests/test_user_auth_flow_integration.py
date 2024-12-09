import pytest
from app.models import User, Todo
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from flask import url_for, session

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.mark.integration
def test_user_authentication_flow(client):
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