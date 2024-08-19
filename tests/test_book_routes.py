import pytest
from app import create_app, db
from app.models import User, Book
import json

@pytest.fixture(scope='module')
def app():
    # Set up the Flask application for testing
    app = create_app('testing')  # Ensure 'testing' configuration is used in create_app
    with app.app_context():
        db.create_all()  # Initialize the database
    yield app  # Yield the app for testing
    with app.app_context():
        db.session.remove()  # Close the session
        db.drop_all()  # Drop all tables

@pytest.fixture
def test_client(app):
    # Provide a test client to interact with the Flask application
    return app.test_client()

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

        # Ensure we get the 'token' from the response
        if 'token' in data:
            return {'Authorization': f"Bearer {data['token']}"}
        else:
            pytest.fail(f"Login failed, response: {data}")

def test_get_books(test_client, auth_header):
    # Test the 'GET /api/books' route
    response = test_client.get('/api/books', headers=auth_header)
    assert response.status_code == 200  # Ensure the route responds successfully

def test_add_book(test_client, auth_header):
    # Test the 'POST /api/books' route for adding a book
    response = test_client.post('/api/books', headers=auth_header, json={
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'science',
        'year_published': 2012
    })
    assert response.status_code == 201  # Ensure the book was successfully added
    data = json.loads(response.data)
    print("******", data)
    assert data['title'] == 'Test Book'  # Verify the title of the added book
    return data['id']  # Return book ID for further tests

def test_get_single_book(test_client, auth_header):
    # Add a book first
    book_id = test_add_book(test_client, auth_header)
    
    # Test the 'GET /api/books/<id>' route
    response = test_client.get(f'/api/books/{book_id}', headers=auth_header)
    assert response.status_code == 200  # Ensure the route responds successfully
    data = json.loads(response.data)
    assert data['id'] == book_id  # Verify the correct book is returned

def test_update_book(test_client, auth_header):
    # Add a book first
    book_id = test_add_book(test_client, auth_header)
    
    # Test the 'PUT /api/books/<id>' route for updating a book
    response = test_client.put(f'/api/books/{book_id}', headers=auth_header, json={
        'title': 'Updated Book Title',
        'author': 'Updated Author',
        'isbn': '0987654321'
    })
    assert response.status_code == 200  # Ensure the book was successfully updated
    data = json.loads(response.data)
    assert data['title'] == 'Updated Book Title'  # Verify the title of the updated book

def test_delete_book(test_client, auth_header):
    # Add a book first
    book_id = test_add_book(test_client, auth_header)
    
    # Test the 'DELETE /api/books/<id>' route
    response = test_client.delete(f'/api/books/{book_id}', headers=auth_header)
    assert response.status_code == 200  # Ensure the book was successfully deleted

    # Verify the book no longer exists
    response = test_client.get(f'/api/books/{book_id}', headers=auth_header)
    assert response.status_code == 404  # Ensure the book no longer exists
