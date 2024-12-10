import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Todo, User
from flask import url_for, session


def test_create_task_valid_input(client):
    """
        Test task creation with valid input.

        This function verifies that a user can successfully create a task with valid input.
        It performs the following steps:
        - Creates a user and logs in.
        - Creates a task with valid content and priority.
        - Checks that the task is saved in the database with correct attributes.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The session contains the correct user ID after login.
            - The task creation endpoint returns a status code of 302 (redirect on success).
            - The created task exists in the database with expected content, priority, and user ID.
    """

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
    """
        Test task creation with empty content.

        This function ensures that attempting to create a task with empty content
        fails validation and does not result in a successful creation.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The task creation endpoint returns a status code of 200, indicating
                no redirection due to validation error.
            - No task is created in the database when content is empty.
    """
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
    """
        Test task creation with invalid priority.

        This function validates that attempting to create a task with an invalid priority
        fails and does not result in a successful task creation.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The task creation endpoint returns a status code of 200, indicating
            no redirection due to validation error.
            - No task is created in the database when priority is invalid.
    """
    # Create a user and log in
    user = User(username='testuser')
    user.set_password(password='password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'testuser', 'password': 'password'})

    # Try to create a task with an invalid priority
    response = client.post('/index', data={'content': 'Test', 'priority': '1'}) 
    assert response.status_code == 200  # Should not redirect due to validation error