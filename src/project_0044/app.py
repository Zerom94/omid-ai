from flask import Flask, request, g, render_template_string, redirect, url_for
import sqlite3
from db import get_db, init_db

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template_string('''
        <h1>Welcome to VulnWeb</h1>
        <p><a href="{{ url_for('login') }}">Login</a></p>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        # Vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = g.db.execute(query)
        user = cur.fetchone()
        if user:
            return f"Hello, {user['username']}! You have logged in successfully."
        else:
            return "Invalid credentials."
    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            Username: <input type="text" name="username"/><br/>
            Password: <input type="password" name="password"/><br/>
            <input type="submit" value="Login"/>
        </form>
    ''')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
