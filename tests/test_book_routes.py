# import pytest
# from app import create_app
# from app.models import User, db

# @pytest.fixture(scope='module')
# def test_client():
#     app = create_app()  # Ensure 'testing' config is being used in create_app
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()  # Initialize the database
#         yield client
#         with app.app_context():
#             db.session.remove()  # Close the session
#             db.drop_all()  # Drop all tables

# @pytest.fixture
# def auth_header(test_client):
#     with test_client.application.app_context():
#         # Check if the user already exists
#         existing_user = User.query.filter_by(email='testuser@example.com').first()
        
#         # If the user does not exist, register the user
#         if existing_user is None:
#             response = test_client.post('/api/register', json={'email': 'testuser@example.com', 'password': 'password'})
#             print(f"Register Response Status Code: {response.status_code}")
#             assert response.status_code == 201, f"Expected 201, got {response.status_code} - {response.json}"

#         # Login the user to get the auth token
#         response = test_client.post('/api/login', json={'email': 'testuser@example.com', 'password': 'password'})
#         print(f"Login Response Status Code: {response.status_code}")
#         assert response.status_code == 200, f"Expected 200, got {response.status_code} - {response.json}"
        
#         token = response.json['token']
#         user = User.query.filter_by(email='testuser@example.com').first()
        
#         return {'Authorization': f'Bearer {token}', 'user_id': user.id}

# # Test cases
# def test_add_book(test_client, auth_header):
#     response = test_client.post('/api/books', json={
#         'title': 'Test Book',
#         'author': 'Test Author',
#         'genre': 'Fiction',
#         'year_published': 2024
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Add Book Response: {response.json}")
#     assert response.status_code == 201, f"Expected 201, got {response.status_code}"

# def test_get_books(test_client, auth_header):
#     # Add a book first
#     test_client.post('/api/books', json={
#         'title': 'Test Book',
#         'author': 'Test Author',
#         'genre': 'Fiction',
#         'year_published': 2024
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     response = test_client.get('/api/books', headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Get Books Response: {response.json}")
#     assert response.status_code == 200
#     assert len(response.json) > 0

# def test_get_book_by_id(test_client, auth_header):
#     # Add a book and retrieve its ID
#     response = test_client.post('/api/books', json={
#         'title': 'Another Test Book',
#         'author': 'Another Author',
#         'genre': 'Non-Fiction',
#         'year_published': 2023
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     book_id = response.json['id']
#     response = test_client.get(f'/api/books/{book_id}', headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Get Book by ID Response: {response.json}")
#     assert response.status_code == 200
#     assert response.json['title'] == 'Another Test Book'

# def test_update_book(test_client, auth_header):
#     # Add a book to update
#     response = test_client.post('/api/books', json={
#         'title': 'Book to Update',
#         'author': 'Author',
#         'genre': 'Drama',
#         'year_published': 2022
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     book_id = response.json['id']
#     response = test_client.put(f'/api/books/{book_id}', json={
#         'title': 'Updated Book Title'
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Update Book Response: {response.json}")
#     assert response.status_code == 200
#     assert response.json['message'] == 'Book updated successfully'

# def test_delete_book(test_client, auth_header):
#     # Add a book to delete
#     response = test_client.post('/api/books', json={
#         'title': 'Book to Delete',
#         'author': 'Author',
#         'genre': 'Sci-Fi',
#         'year_published': 2021
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     book_id = response.json['id']
#     response = test_client.delete(f'/api/books/{book_id}', headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Delete Book Response: {response.json}")
#     assert response.status_code == 200
#     assert response.json['message'] == 'Book deleted successfully'

# def test_add_review(test_client, auth_header):
#     # Add a book first
#     response = test_client.post('/api/books', json={
#         'title': 'Book for Review',
#         'author': 'Author',
#         'genre': 'Fantasy',
#         'year_published': 2020
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     book_id = response.json['id']
#     response = test_client.post(f'/api/books/{book_id}/reviews', json={
#         'user_id': auth_header['user_id'],
#         'review_text': 'Great book!',
#         'rating': 5
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Add Review Response: {response.json}")
#     assert response.status_code == 201, f"Expected 201, got {response.status_code}"

# def test_get_reviews(test_client, auth_header):
#     # Add a book and review
#     response = test_client.post('/api/books', json={
#         'title': 'Book for Reviews',
#         'author': 'Author',
#         'genre': 'Mystery',
#         'year_published': 2024
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     book_id = response.json['id']
#     test_client.post(f'/api/books/{book_id}/reviews', json={
#         'user_id': auth_header['user_id'],
#         'review_text': 'Interesting read!',
#         'rating': 4
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     response = test_client.get(f'/api/books/{book_id}/reviews', headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Get Reviews Response: {response.json}")
#     assert response.status_code == 200
#     assert len(response.json) > 0

# def test_get_book_summary(test_client, auth_header):
#     # Add a book
#     response = test_client.post('/api/books', json={
#         'title': 'Book Summary',
#         'author': 'Author',
#         'genre': 'Biography',
#         'year_published': 2025
#     }, headers={'Authorization': auth_header['Authorization']})
    
#     book_id = response.json['id']
#     response = test_client.get(f'/api/books/{book_id}/summary', headers={'Authorization': auth_header['Authorization']})
    
#     print(f"Get Book Summary Response: {response.json}")
#     assert response.status_code == 200
#     assert 'title' in response.json
#     assert 'average_rating' in response.json

import pytest
from app import create_app
from app.models import User, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Initialize the database
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_header(test_client):
    # Ensure the test client runs within the app context
    with test_client.application.app_context():
        # Check if user exists, if not register the user
        existing_user = User.query.filter_by(email='testuser@example.com').first()
        if not existing_user:
            response = test_client.post('/api/register', json={'email': 'testuser@example.com', 'password': 'password'})
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        # Login to get the token
        response = test_client.post('/api/login', json={'email': 'testuser@example.com', 'password': 'password'})
        assert response.status_code == 200
        token = response.json['token']
        user = User.query.filter_by(email='testuser@example.com').first()
        
        return {'Authorization': f'Bearer {token}', 'user_id': user.id}

def test_add_book(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'year_published': 2024
        }, headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 201
        assert 'id' in response.json, f"Expected 'id' in response, got {response.json}"

def test_get_books(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'year_published': 2024
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json['id']
        response = test_client.get('/api/books', headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 200
        assert len(response.json) > 0

def test_get_book_by_id(test_client, auth_header):
    with test_client.application.app_context():
        # First, add a book to get its ID
        response = test_client.post('/api/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'year_published': 2024
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json.get('id', None)
        assert book_id is not None, "Book ID not found in response."
        
        response = test_client.get(f'/api/books/{book_id}', headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 200
        assert response.json['id'] == book_id

def test_update_book(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Book to Update',
            'author': 'Author',
            'genre': 'Drama',
            'year_published': 2022
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json.get('id', None)
        assert book_id is not None, "Book ID not found in response."
        
        response = test_client.put(f'/api/books/{book_id}', json={
            'title': 'Updated Book Title'
        }, headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 200
        assert response.json['message'] == 'Book updated successfully'

def test_delete_book(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Book to Delete',
            'author': 'Author',
            'genre': 'Sci-Fi',
            'year_published': 2021
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json.get('id', None)
        assert book_id is not None, "Book ID not found in response."
        
        response = test_client.delete(f'/api/books/{book_id}', headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 200
        assert response.json['message'] == 'Book deleted successfully'

def test_add_review(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Book for Review',
            'author': 'Author',
            'genre': 'Fantasy',
            'year_published': 2020
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json.get('id', None)
        assert book_id is not None, "Book ID not found in response."
        
        response = test_client.post(f'/api/books/{book_id}/reviews', json={
            'user_id': auth_header['user_id'],
            'review_text': 'Great book!',
            'rating': 5
        }, headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 201

def test_get_reviews(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Book for Reviews',
            'author': 'Author',
            'genre': 'Mystery',
            'year_published': 2024
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json.get('id', None)
        assert book_id is not None, "Book ID not found in response."
        
        response = test_client.get(f'/api/books/{book_id}/reviews', headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 200
        assert len(response.json) > 0

def test_get_book_summary(test_client, auth_header):
    with test_client.application.app_context():
        response = test_client.post('/api/books', json={
            'title': 'Book Summary',
            'author': 'Author',
            'genre': 'Biography',
            'year_published': 2025
        }, headers={'Authorization': auth_header['Authorization']})
        
        book_id = response.json.get('id', None)
        assert book_id is not None, "Book ID not found in response."
        
        response = test_client.get(f'/api/books/{book_id}/summary', headers={'Authorization': auth_header['Authorization']})
        
        assert response.status_code == 200
        assert 'title' in response.json
        assert 'average_rating' in response.json

