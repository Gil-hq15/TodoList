import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import User, Todo
from app import create_app, db
from flask import url_for, session, current_app
from playwright.sync_api import sync_playwright

@pytest.fixture
def client():
    """
        Fixture to create and configure a Flask test client for use in integration tests.

        This fixture initializes a Flask app in 'production' mode, sets up the app context,
        creates the necessary database tables, and provides a test client to simulate HTTP 
        requests during testing. After the test, the fixture ensures that the database session 
        is removed and all tables are dropped to clean up the test environment.

        Yields:
            client: A Flask test client used to make HTTP requests.
    """
    app = create_app('production')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
def browser(request):
    """
        Fixture to create and configure a Playwright browser instance for UI testing.

        This fixture sets up a Playwright browser instance that can be used to simulate
        user interactions with the app in different browsers (Chromium, Firefox, or WebKit).
        The browser is launched in headless mode to run automated tests without a graphical 
        interface. The fixture is parameterized to test across multiple browsers.

        Parameters:
            request (pytest.FixtureRequest): The request object, which allows accessing the 
                                            parameterized browser type.

        Yields:
            browser: A Playwright browser instance for use in the test.
    """
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch(headless=True)
        yield browser
        browser.close()
