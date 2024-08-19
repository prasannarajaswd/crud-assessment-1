import pytest
from app import create_app, db
from app.models import User, Book  # Assuming models include User and Book
import json

@pytest.fixture(scope='module')
def test_client():
    # Set up the Flask application for testing
    app = create_app('testing')  # Ensure 'testing' configuration is used in create_app
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Initialize the database
        yield client  # Yield the client for testing
        with app.app_context():
            db.session.remove()  # Close the session
            db.drop_all()  # Drop all tables

@pytest.fixture
def auth_header(test_client):
    # Register and log in a user to obtain an authentication token
    with test_client.application.app_context():
        # Register the user
        test_client.post('/api/register', json={
            'email': 'testuser@example.com',
            'password': 'password'
        })

        # Log in the user to get a token
        login_response = test_client.post('/api/login', json={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        data = json.loads(login_response.data)
        return {'Authorization': f"Bearer {data['access_token']}"}

def test_get_books(test_client, auth_header):
    # Test the 'GET /api/books' route
    response = test_client.get('/api/books', headers=auth_header)
    assert response.status_code == 200  # Ensure the route responds successfully

def test_add_book(test_client, auth_header):
    # Test the 'POST /api/books' route for adding a book
    response = test_client.post('/api/books', headers=auth_header, json={
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '1234567890'
    })
    assert response.status_code == 201  # Ensure the book was successfully added
    data = json.loads(response.data)
    assert data['title'] == 'Test Book'  # Verify the title of the added book

def test_register_user(test_client):
    # Test the 'POST /api/register' route for user registration
    response = test_client.post('/api/register', json={
        'email': 'newuser@example.com',
        'password': 'password'
    })
    assert response.status_code == 201  # Ensure user was registered successfully
    data = json.loads(response.data)
    assert data['email'] == 'newuser@example.com'  # Verify the user's email
