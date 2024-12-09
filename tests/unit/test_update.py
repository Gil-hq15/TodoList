import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Todo, User

def test_update_task(client):
    # Create a user and log in
    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'testuser', 'password': 'password'})

    # Create a task
    task = Todo(content='Original Task', priority='Low', user_id=user.id)
    db.session.add(task)
    db.session.commit()

    # Update the task
    response = client.post(f'/update/{task.id}', data={
        'content': 'Updated Task',
        'priority': 'High'
    })
    
    assert response.status_code == 302  # Check for successful redirect

    # Verify the task was updated
    updated_task = Todo.query.get(task.id)
    assert updated_task is not None
    assert updated_task.content == 'Updated Task'
    assert updated_task.priority == 'High'