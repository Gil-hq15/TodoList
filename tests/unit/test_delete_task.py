from app import create_app, db
from app.models import Todo, User


def test_delete_task_valid_id(client):
    """
        Test task deletion with a valid task ID.

        This function verifies that a task is successfully deleted when a valid task ID is provided:
        - Creates a user and logs in.
        - Creates a task associated with the user.
        - Sends a request to delete the task using its ID.
        - Validates that the task is removed from the database.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The delete endpoint returns a status code of 302 (indicating success).
            - The task no longer exists in the database after deletion.
    """
    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    client.post('/', data={'username': 'testuser', 'password': 'password'})
    
    task = Todo(content='Test task', priority='High', user_id=user.id)
    db.session.add(task)
    db.session.commit()

    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302  
    deleted_task = Todo.query.get(task.id)
    assert deleted_task is None  

def test_delete_task_invalid_id(client):
    """
        Test task deletion with an invalid task ID.

        This function ensures that attempting to delete a task with an invalid ID:
        - Results in a 404 status code response.

        Args:
            client: Flask testing client instance.

        Returns:
            None. The test asserts that:
            - The delete endpoint returns a status code of 404 when a non-existent task ID is used.
    """
    client.post('/', data={'username': 'testuser', 'password': 'password'})
    
    response = client.get('/delete/9999')  
    assert response.status_code == 404  
