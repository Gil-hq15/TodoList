from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
oauth = OAuth()

def create_app(config_name='Config'):
    app = Flask(__name__)

    # Load configuration
    config_class = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }.get(config_name, Config)

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    oauth.init_app(app)

    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={'scope': 'openid email profile'},
    )

    # Import models to ensure they are registered with SQLAlchemy
    with app.app_context():
        from app.models import User, Todo # Import your User model (and any others)
        db.create_all()  # Creates tables if they don't exist (development use only)

    # Register blueprints
    from app.routes.main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app