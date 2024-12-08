from flask import Blueprint, render_template, request, redirect, session, url_for
from app import oauth, db
from app.models import Todo, User, db
import secrets

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect('/index')
        else:
            return render_template('login.html', oauth_login_url=url_for('main.oauth_login'), error='Invalid username or password. Try again.')
    return render_template('login.html', oauth_login_url=url_for('main.oauth_login'))

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password1']
        if password != password_confirm:
            return render_template('register.html', error='The passwords do not match. Please try again.')
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists.')
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
            return render_template('index.html', username=User.query.get(session['user_id']).username, tasks=tasks, error='Task with no content.')
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
            user = User(username=user_info['name'], password_hashed='oauth') 
            db.session.add(user)
            db.session.commit()

        session['user_id'] = user.id
        return redirect('/index')

    except Exception as e:
        return f'Error during OAuth callback: {str(e)}'

@main_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')