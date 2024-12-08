import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Todo, User
from flask import url_for

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
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    
    response = client.post('/index', data={'content': 'Test task', 'priority': '1'})
    assert response.status_code == 302 

    task = Todo.query.first()
    assert task is not None
    assert task.content == 'Test task'
    assert task.priority == '1'

def test_create_task_empty_content(client):
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/index', data={'content': '', 'priority': '1'})
    assert response.status_code == 200  

def test_create_task_invalid_priority(client):
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/index', data={'content': 'Test', 'priority': 'high'})
    assert response.status_code == 200 
