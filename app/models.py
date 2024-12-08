from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.utc))

    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)