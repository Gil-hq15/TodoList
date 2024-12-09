import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Todo, User
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


def test_create_task_valid_input(client):
    # Create a user and log in
    user = User(username='testuser')
    user.set_password(password='password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'testuser', 'password': 'password'})

    print(f"Session after login: {client.session_transaction()}")
    with client.session_transaction() as session:
        assert session['user_id'] == user.id
    
    # Create a task
    response = client.post('/index', data={'content': 'Test task', 'priority': 'High'})
    assert response.status_code == 302  # Redirect indicates success

    # Verify task in database
    task = Todo.query.first()
    assert task is not None
    assert task.content == 'Test task'
    assert task.priority == 'High'
    assert task.user_id == user.id


def test_create_task_empty_content(client):
    # Create a user and log in
    user = User(username='testuser')
    user.set_password(password='password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'testuser', 'password': 'password'})

    # Try to create a task with empty content
    response = client.post('/index', data={'content': '', 'priority': 'High'})
    assert response.status_code == 200  # Should not redirect due to validation error


def test_create_task_invalid_priority(client):
    # Create a user and log in
    user = User(username='testuser')
    user.set_password(password='password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'testuser', 'password': 'password'})

    # Try to create a task with an invalid priority
    response = client.post('/index', data={'content': 'Test', 'priority': '1'}) 
    assert response.status_code == 200  # Should not redirect due to validation error