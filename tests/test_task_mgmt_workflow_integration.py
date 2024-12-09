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
def test_task_management_workflow(client):
    # Create and log in a user
    user = User(username='taskuser')
    user.set_password('hashed_password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'taskuser', 'password': 'hashed_password'})

    # Create a task
    response = client.post('/index', data={'content': 'Task 1', 'priority': 'High'})
    assert response.status_code == 302  # Redirect indicates success

    # Update the task
    task = Todo.query.filter_by(content='Task 1').first()
    response = client.post(f'/update/{task.id}', data={'content': 'Updated Task', 'priority': 'Medium'})
    assert response.status_code == 302

    # Verify task update
    updated_task = Todo.query.filter_by(id=task.id).first()
    assert updated_task.content == 'Updated Task'
    assert updated_task.priority == 'Medium'

    # Delete the task
    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302

    # Verify task deletion
    deleted_task = Todo.query.filter_by(id=task.id).first()
    assert deleted_task is None