import secrets
import requests
import random
from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from app import oauth, db, Config
from app.models import Todo, User, db
from datetime import datetime, timedelta

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id

            nasa_api_key = current_app.config['NASA_API_KEY']
            random_date = generate_random_date()
            response = requests.get(
                'https://api.nasa.gov/planetary/apod',
                params={'api_key': nasa_api_key, 'date': random_date}
            )
            if response.status_code == 200:
                nasa_data = response.json()
                session['nasa_apod'] = {
                    'date': nasa_data['date'],
                    'title': nasa_data['title'],
                    'image_url': nasa_data['url'],
                    'explanation': nasa_data['explanation']
                }
            else:
                session['nasa_apod'] = {'error': 'Failed to fetch NASA APOD.'}

            return redirect('/index')
        else:
            return render_template('login.html', oauth_login_url=url_for('main.oauth_login'), error='Invalid username or password. Try again.'), 200
    return render_template('login.html', oauth_login_url=url_for('main.oauth_login'))

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password1']
        if password != password_confirm:
            return render_template('register.html', error='The passwords do not match. Please try again.'), 200
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists.'), 200
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@main_blueprint.route('/index', methods=['POST', 'GET'])
def index():
    if 'user_id' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form['priority']
        if len(task_content)==0:
            tasks = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.date_created).all()
            return render_template('index.html', username=User.query.get(session['user_id']).username, tasks=tasks, error='Task with no content.'), 200
        
        allowed_priorities = ['High', 'Medium', 'Low']
        if task_priority not in allowed_priorities:
            tasks = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.date_created).all()
            return render_template('index.html', username=User.query.get(session['user_id']).username, tasks=tasks, error='Invalid priority.'), 200
        new_task = Todo(content=task_content, priority=task_priority, user_id=session['user_id'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/index')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.date_created).all()
        return render_template('index.html', username=User.query.get(session['user_id']).username, tasks=tasks)

@main_blueprint.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/index')
    except:
        return 'There was a problem deleting that task'

@main_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.priority = request.form['priority']

        try:
            db.session.commit()
            return redirect('/index')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
    

@main_blueprint.route('/oauth-login')
def oauth_login():
    nonce = secrets.token_urlsafe(16)  # Generate a secure random nonce
    session['nonce'] = nonce

    redirect_uri = url_for('main.oauth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@main_blueprint.route('/oauth-callback')
def oauth_callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token, nonce=session['nonce'])

        session['user'] = {
            'id': user_info['sub'], 
            'name': user_info['name'],
            'email': user_info['email']
        }

        user = User.query.filter_by(username=user_info['name']).first()
        if not user:
            user = User(username=user_info['name']) 
            user.set_password('oauth')
            db.session.add(user)
            db.session.commit()

        session['user_id'] = user.id

        nasa_api_key = current_app.config['NASA_API_KEY']
        random_date = generate_random_date()
        response = requests.get(
            'https://api.nasa.gov/planetary/apod',
            params={'api_key': nasa_api_key, 'date': random_date}
        )
        if response.status_code == 200:
            nasa_data = response.json()
            session['nasa_apod'] = {
                'date': nasa_data['date'],
                'title': nasa_data['title'],
                'image_url': nasa_data['url'],
                'explanation': nasa_data['explanation']
            }
        else:
            session['nasa_apod'] = {'error': 'Failed to fetch NASA APOD.'}
        return redirect('/index')

    except Exception as e:
        return f'Error during OAuth callback: {str(e)}'

@main_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

def generate_random_date():
    """Generate a random date within the range of the NASA APOD API (June 16, 1995 - today)."""
    start_date = datetime(1995, 6, 16)
    end_date = datetime.now()
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')