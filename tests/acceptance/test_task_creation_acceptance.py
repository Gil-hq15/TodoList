import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User
from flask import current_app
from dotenv import load_dotenv

load_dotenv()  

def test_task_creation(client, browser):
    page = browser.new_page()

    url = os.getenv('URL')
    # Navigate to the registration page
    page.goto(url + "/register")
    
    # Fill out the registration form
    page.fill("input[name='username']", "test-user")
    page.fill("input[name='password']", "testpassword")
    page.fill("input[name='password1']", "testpassword")
    page.click("button:has-text('Create Account')")

    # Log in as a test user
    page.fill("input[name='username']", "test-user")
    page.fill("input[name='password']", "testpassword")
    page.click("button:has-text('Log In')")

    # Create a task
    page.fill("input[name='content']", "Sample Task")
    page.select_option("select[name='priority']", "High")
    page.click("input[type='submit']")

    assert "Sample Task" in page.content()

    # Clean up: Remove the user created during the test
    with client.application.app_context():
        user = User.query.filter_by(username="test-user").first()
        if user:
            db.session.delete(user)
            db.session.commit()