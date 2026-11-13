from flask import Flask, request
from db import query_user

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>VulnWeb</h1>
    <form action="/login" method="GET">
      Username: <input name="username"><br>
      <input type="submit" value="Login">
    </form>
    '''

@app.route('/login')
def login():
    username = request.args.get('username', '')
    # Vulnerable to SQL injection
    user = query_user(username)
    if user:
        return f"Welcome, {user['username']}! Your secret: {user['secret']}"
    else:
        return "User not found"

if __name__ == '__main__':
    app.run(debug=True)
