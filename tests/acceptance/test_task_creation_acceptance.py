import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User
from flask import current_app


def test_task_creation(client, browser, request):
    """
        Test task creation workflow using a browser.

        This function tests the end-to-end task creation process, including:
        - User registration.
        - User login.
        - Task creation with valid input.
        - Validation that the created task appears on the user's page.

        Args:
            client: Flask testing client instance.
            browser: Browser automation instance (e.g., Playwright browser context).
            request: Test request object to access parameterized data (e.g., browser name).

        Returns:
            None. The test asserts that:
            - The created task is visible on the page after submission.
            - User and task workflows function as expected.
            - Test data is cleaned up by removing the created user from the database.
    """
    browser_name = request.node.callspec.params["browser"]
    context = browser.new_context()
    page = context.new_page()

    URL = current_app.config['URL']
    # Navigate to the registration page
    page.goto(URL + "/register")

    # Fill out the registration form
    page.fill("input[name='username']", "test-user-" + browser_name)
    page.fill("input[name='password']", "testpassword")
    page.fill("input[name='password1']", "testpassword")
    page.click("button:has-text('Create Account')")

    # Log in as a test user
    page.fill("input[name='username']", "test-user-" + browser_name)
    page.fill("input[name='password']", "testpassword")
    page.click("button:has-text('Log In')")

    # Create a task
    page.fill("input[name='content']", "Sample Task")
    page.select_option("select[name='priority']", "High")
    page.click("input[type='submit']")

    assert "Sample Task" in page.content()

    # Clean up: Remove the user created during the test
    with client.application.app_context():
        user = User.query.filter_by(username="test-user-" + browser_name).first()
        if user:
            db.session.delete(user)
            db.session.commit()