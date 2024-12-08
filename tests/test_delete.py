import pytest
from app import create_app, db
from app.models import Todo, User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_delete_task_valid_id(client):
    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    
    task = Todo(content='Test task', priority='High', user_id=user.id)
    db.session.add(task)
    db.session.commit()

    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302  
    deleted_task = Todo.query.get(task.id)
    assert deleted_task is None  

def test_delete_task_invalid_id(client):
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    
    response = client.get('/delete/9999')  
    assert response.status_code == 404  
