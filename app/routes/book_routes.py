from flask import Blueprint, request, jsonify
from app.models import Book, Review, db
from app.services.auth_service import token_required
from sqlalchemy import func

book_bp = Blueprint('book_bp', __name__)

# 1. Add a new book (POST /books)
@book_bp.route('/books', methods=['POST'])
@token_required
def add_book(current_user):
    data = request.get_json()

    # Ensure required fields are present
    if not all(key in data for key in ('title', 'author', 'genre', 'year_published')):
        return jsonify({'message': 'Missing required fields'}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        year_published=data['year_published']
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({
        'message': 'Book added successfully', 
        'title': new_book.title, 
        'id': new_book.id
    }), 201

# 2. Retrieve all books (GET /books)
@book_bp.route('/books', methods=['GET'])
@token_required
def get_books(current_user):
    books = Book.query.all()
    book_list = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'year_published': book.year_published,
        'summary': book.summary
    } for book in books]
    return jsonify(book_list), 200

# 3. Retrieve a specific book by its ID (GET /books/<id>)
@book_bp.route('/books/<int:id>', methods=['GET'])
@token_required
def get_book_by_id(current_user, id):
    book = Book.query.get_or_404(id)
    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'year_published': book.year_published,
        'summary': book.summary
    }
    return jsonify(book_data), 200

# 4. Update a book's information by its ID (PUT /books/<id>)
@book_bp.route('/books/<int:id>', methods=['PUT'])
@token_required
def update_book(current_user, id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    # Update fields if present
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.year_published = data.get('year_published', book.year_published)
    book.summary = data.get('summary', book.summary)

    db.session.commit()
    return jsonify({
        'message': 'Book added successfully', 
        'title': book.title, 
        'id': book.id
    }), 200

# 5. Delete a book by its ID (DELETE /books/<id>)
@book_bp.route('/books/<int:id>', methods=['DELETE'])
@token_required
def delete_book(current_user, id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

# 6. Add a review for a book (POST /books/<id>/reviews)
@book_bp.route('/books/<int:id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    # Ensure required fields are present
    if not all(key in data for key in ('user_id', 'review_text', 'rating')):
        return jsonify({'message': 'Missing required fields'}), 400

    new_review = Review(
        book_id=book.id,
        user_id=data['user_id'],
        review_text=data['review_text'],
        rating=data['rating']
    )

    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully'}), 201

# 7. Retrieve all reviews for a book (GET /books/<int:id>/reviews)
@book_bp.route('/books/<int:id>/reviews', methods=['GET'])
@token_required
def get_reviews(current_user, id):
    book = Book.query.get_or_404(id)
    reviews = Review.query.filter_by(book_id=book.id).all()

    review_list = [{
        'id': review.id,
        'user_id': review.user_id,
        'review_text': review.review_text,
        'rating': review.rating
    } for review in reviews]

    return jsonify(review_list), 200

# 8. Get a summary and aggregated rating for a book (GET /books/<int:id>/summary)
@book_bp.route('/books/<int:id>/summary', methods=['GET'])
@token_required
def get_book_summary(current_user, id):
    book = Book.query.get_or_404(id)

    # Assuming summary generation via an external service/model
    summary = book.summary  # Placeholder for AI summary generation

    # Aggregate rating
    avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.book_id == id).scalar()

    response = {
        'title': book.title,
        'author': book.author,
        'summary': summary,
        'average_rating': avg_rating if avg_rating else 'No ratings yet'
    }

    return jsonify(response), 200

# 9. Get book recommendations based on user preferences (GET /recommendations)
@book_bp.route('/recommendations', methods=['GET'])
@token_required
def get_recommendations(current_user):
    # Assuming some logic or model to generate recommendations
    # Placeholder logic: Recommend random books for now
    books = Book.query.order_by(func.random()).limit(5).all()

    recommended_books = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre
    } for book in books]

    return jsonify(recommended_books), 200
