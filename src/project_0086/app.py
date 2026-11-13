import sqlite3
import os
from flask import Flask, request, g, render_template, redirect, url_for

app = Flask(__name__)
DATABASE = 'vuln.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        cursor.execute('INSERT OR IGNORE INTO users (id, username, password) VALUES (1, "admin", "admin")')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Vulnerable to SQL injection
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = get_db().execute(query)
        user = cur.fetchone()
        if user:
            return f"Welcome, {username}!"
        else:
            return "Invalid credentials"
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/search')
def search():
    q = request.args.get('q', '')
    # Vulnerable to command injection
    result = os.popen(f'echo Searching for: {q}').read()
    return f"<pre>{result}</pre>"

@app.route('/xss')
def xss():
    payload = request.args.get('payload', '')
    # Reflected XSS
    return f"<h1>{payload}</h1>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
