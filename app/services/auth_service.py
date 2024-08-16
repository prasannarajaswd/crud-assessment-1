import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from app.models import User
from app import db
from app.config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if Authorization header exists
        if 'Authorization' in request.headers:
            try:
                # Attempt to extract the token from the Authorization header
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token format is invalid!'}), 401
        else:
            return jsonify({'message': 'Authorization header is missing!'}), 401

        # If the token is missing after extraction
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
            
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def generate_token(user):
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expiry time set to 24 hours
    }, Config.SECRET_KEY, algorithm="HS256")

    return token
