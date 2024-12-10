import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import User, Todo
from app import create_app, db
from flask import url_for, session
from playwright.sync_api import sync_playwright

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

"""@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()"""

@pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
def browser(request):
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch(headless=True)
        yield browser
        browser.close()
