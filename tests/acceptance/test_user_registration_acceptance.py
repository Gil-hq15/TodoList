import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User
from flask import current_app


def test_user_registration(client, browser, request):
    """
        Test user registration workflow using a browser.

        This function verifies that the user registration process works as expected,
        including filling out the registration form and checking that the user is
        redirected to the login page upon successful registration.

        Args:
            client: Flask testing client instance.
            browser: Browser automation instance (e.g., Playwright browser context).
            request: Test request object to access parameterized data (e.g., browser name).

        Returns:
            None. The test asserts that:
            - The user is redirected to the login page ("/") after successful registration.
            - Test data is cleaned up by removing the created user from the database.
    """
    browser_name = request.node.callspec.params["browser"]
    context = browser.new_context()
    page = context.new_page()
    URL = current_app.config['URL']

    # Navigate to the registration page
    page.goto(URL + "/register")

    # Fill out the registration form
    page.fill("input[name='username']", "test-user" + browser_name)
    page.fill("input[name='password']", "testpassword")
    page.fill("input[name='password1']", "testpassword")
    page.click("button:has-text('Create Account')")
    
    # Assert that we are redirected to the login page
    assert page.url == URL + "/"

    # Clean up: Remove the user created during the test
    with client.application.app_context():
        user = User.query.filter_by(username="test-user" + browser_name).first()
        if user:
            db.session.delete(user)
            db.session.commit()
