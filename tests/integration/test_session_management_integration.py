import pytest
from app.models import User, Todo
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from flask import url_for, session


@pytest.mark.integration
def test_session_management(client):
    # Log in a user
    user = User(username='sessionuser')
    user.set_password('hashed_password')
    db.session.add(user)
    db.session.commit()

    client.post('/', data={'username': 'sessionuser', 'password': 'hashed_password'})

    # Verify session contains user ID
    with client.session_transaction() as session:
        print(session)
        assert 'user_id' in session
        assert session['user_id'] == user.id

    # Log out the user
    client.get('/logout')

    # Verify session is cleared
    with client.session_transaction() as session:
        assert 'user_id' not in session