import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Todo, User

def test_update_task(client):
    """
        Test task update functionality.

        This function verifies that a task can be successfully updated:
        - Creates a user and logs in.
        - Creates a task for the user with initial values.
        - Sends a request to update the task's content and priority.
        - Verifies that the task is updated in the database.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The update request returns a status code of 302 (indicating a successful redirect).
            - The task is updated with the new content and priority values.
    """
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