from flask import Blueprint, request, jsonify
from app.models import User, db
from app.services.auth_service import generate_token, token_required

user_bp = Blueprint('user_bp', __name__)

# User Registration
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing fields'}), 400

    # Check if the username or email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'email already exists'}), 409

    # Create a new user
    new_user = User(email=data['email'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing fields'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate token for the user
    token = generate_token(user)

    return jsonify({'token': token}), 200

# Protected route example
@user_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    user_data = {
        'id': current_user.id,
        'email': current_user.email
    }

    return jsonify(user_data), 200
