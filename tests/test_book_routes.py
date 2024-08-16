import pytest
from app import create_app
from app.models import User, Book, Review, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app()  # Make sure you have a 'testing' config
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            print(app.url_map)  # Print all registered routes
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_header(test_client):
    # Register and login a user to get the auth token
    response = test_client.post('register', json={'email': 'testuser@example.com', 'password': 'password'})
    assert response.status_code == 201
    
    response = test_client.post('login', json={'email': 'testuser@example.com', 'password': 'password'})
    assert response.status_code == 200
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}

def test_add_book(test_client, auth_header):
    response = test_client.post('/books', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Fiction',
        'year_published': 2024
    }, headers=auth_header)
    
    assert response.status_code == 201
    assert response.json['message'] == 'Book added successfully'

def test_get_books(test_client, auth_header):
    # Add a book to test retrieval
    test_client.post('/books', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Fiction',
        'year_published': 2024
    }, headers=auth_header)
    
    response = test_client.get('/books', headers=auth_header)
    
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_book_by_id(test_client, auth_header):
    # Add a book and get its ID
    response = test_client.post('/books', json={
        'title': 'Another Test Book',
        'author': 'Another Author',
        'genre': 'Non-Fiction',
        'year_published': 2023
    }, headers=auth_header)
    
    book_id = response.json['id']
    response = test_client.get(f'/books/{book_id}', headers=auth_header)
    
    assert response.status_code == 200
    assert response.json['title'] == 'Another Test Book'

def test_update_book(test_client, auth_header):
    # Add a book to update
    response = test_client.post('/books', json={
        'title': 'Book to Update',
        'author': 'Author',
        'genre': 'Drama',
        'year_published': 2022
    }, headers=auth_header)
    
    book_id = response.json['id']
    response = test_client.put(f'/books/{book_id}', json={
        'title': 'Updated Book Title'
    }, headers=auth_header)
    
    assert response.status_code == 200
    assert response.json['message'] == 'Book updated successfully'

def test_delete_book(test_client, auth_header):
    # Add a book to delete
    response = test_client.post('/books', json={
        'title': 'Book to Delete',
        'author': 'Author',
        'genre': 'Sci-Fi',
        'year_published': 2021
    }, headers=auth_header)
    
    book_id = response.json['id']
    response = test_client.delete(f'/books/{book_id}', headers=auth_header)
    
    assert response.status_code == 200
    assert response.json['message'] == 'Book deleted successfully'

def test_add_review(test_client, auth_header):
    # Add a book first
    response = test_client.post('/books', json={
        'title': 'Book for Review',
        'author': 'Author',
        'genre': 'Fantasy',
        'year_published': 2020
    }, headers=auth_header)
    
    book_id = response.json['id']
    response = test_client.post(f'/books/{book_id}/reviews', json={
        'user_id': 1,  # Assuming user ID is 1 for this example
        'review_text': 'Great book!',
        'rating': 5
    }, headers=auth_header)
    
    assert response.status_code == 201
    assert response.json['message'] == 'Review added successfully'

def test_get_reviews(test_client, auth_header):
    # Add a book and review
    response = test_client.post('/books', json={
        'title': 'Book for Reviews',
        'author': 'Author',
        'genre': 'Mystery',
        'year_published': 2024
    }, headers=auth_header)
    
    book_id = response.json['id']
    test_client.post(f'/books/{book_id}/reviews', json={
        'user_id': 1,
        'review_text': 'Interesting read!',
        'rating': 4
    }, headers=auth_header)
    
    response = test_client.get(f'/books/{book_id}/reviews', headers=auth_header)
    
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_book_summary(test_client, auth_header):
    # Add a book
    response = test_client.post('/books', json={
        'title': 'Book Summary',
        'author': 'Author',
        'genre': 'Biography',
        'year_published': 2025
    }, headers=auth_header)
    
    book_id = response.json['id']
    response = test_client.get(f'/books/{book_id}/summary', headers=auth_header)
    
    assert response.status_code == 200
    assert 'title' in response.json
    assert 'average_rating' in response.json
