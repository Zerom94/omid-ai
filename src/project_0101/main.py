from flask import Flask, request, jsonify

from config import Config
from models import db, User
from auth import register_user, login_user, token_required

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Create DB tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    result, status = register_user(username, password)
    return jsonify(result), status

@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    result, status = login_user(username, password)
    return jsonify(result), status

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello, {current_user.username}! This is a protected resource.'})

if __name__ == '__main__':
    # For development only; use a proper WSGI server in production
    app.run(host='0.0.0.0', port=5000, debug=True)
