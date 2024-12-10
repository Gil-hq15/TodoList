import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User
from flask import current_app


def test_user_registration(client, browser):
    context = browser.new_context()
    page = browser.new_page()
    URL = current_app.config['URL']

    # Navigate to the registration page
    page.goto(URL + "/register")
    
    with client.application.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        
    # Fill out the registration form
    page.fill("input[name='username']", "test-user")
    page.fill("input[name='password']", "testpassword")
    page.fill("input[name='password1']", "testpassword")
    page.click("button:has-text('Create Account')")
    
    # Assert that we are redirected to the login page
    assert page.url == URL + "/"

    # Clean up: Remove the user created during the test
    with client.application.app_context():
        user = User.query.filter_by(username="test-user").first()
        if user:
            db.session.delete(user)
            db.session.commit()
