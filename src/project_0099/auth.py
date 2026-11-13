import os
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, current_app
from models import User, db

def register_user(username: str, password: str) -> User:
    if User.query.filter_by(username=username).first():
        raise ValueError('Username already exists')
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate_user(username: str, password: str) -> str:
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        # jwt.encode returns bytes in pyjwt<2, str in pyjwt>=2
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token
    return None

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except (jwt.InvalidTokenError, Exception):
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
