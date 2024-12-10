import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import User, Todo
from app import create_app, db
from flask import url_for, session

@pytest.mark.integration
def test_task_management_workflow(client):
    """
        Test task management workflow, including creation, updating, and deletion of tasks.

        This function verifies the full workflow for managing tasks:
        - Task creation with valid input.
        - Task updating to modify content and priority.
        - Task deletion and validation of its removal from the database.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - A task is successfully created and saved in the database.
            - The task is updated with new content and priority values.
            - The task is deleted and no longer exists in the database.
    """
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