import datetime
import functools

import bcrypt
import jwt
from flask import request, jsonify, current_app

from models import db, User


def _hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    salt = bcrypt.gensalt(rounds=current_app.config['BCRYPT_LOG_ROUNDS'])
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def _check_password(password: str, hashed: str) -> bool:
    """Verify a password against the stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def _generate_token(user: User) -> str:
    """Create a JWT token for the given user."""
    payload = {
        'sub': user.id,
        'username': user.username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    # PyJWT 2.x returns a string, 1.x returns bytes
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def register_user(username: str, password: str):
    """Create a new user. Returns (result_dict, status_code)."""
    if User.query.filter_by(username=username).first():
        return {'message': 'Username already exists.'}, 409
    password_hash = _hash_password(password)
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'User registered successfully.'}, 201


def login_user(username: str, password: str):
    """Authenticate user and return a JWT token if successful."""
    user = User.query.filter_by(username=username).first()
    if not user or not _check_password(password, user.password_hash):
        return {'message': 'Invalid username or password.'}, 401
    token = _generate_token(user)
    return {'token': token}, 200


def token_required(f):
    """Decorator that checks for a valid JWT token in the Authorization header."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token is missing.'}), 401
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['sub'])
            if not user:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token.'}), 401
        # Pass the current user to the route
        return f(current_user=user, *args, **kwargs)
    return decorated
