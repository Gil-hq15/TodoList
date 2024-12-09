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
def test_database_operations(client):
    # Create a new user
    user = User(username='testuser')
    user.set_password('hashed_password')
    db.session.add(user)
    db.session.commit()

    # Verify user exists in the database
    retrieved_user = User.query.filter_by(username='testuser').first()
    assert retrieved_user is not None
    assert retrieved_user.username == 'testuser'

    # Create a task for the user
    task = Todo(content='Sample Task', priority='High', user_id=retrieved_user.id)
    db.session.add(task)
    db.session.commit()

    # Verify task exists in the database
    retrieved_task = Todo.query.filter_by(content='Sample Task').first()
    assert retrieved_task is not None
    assert retrieved_task.priority == 'High'
