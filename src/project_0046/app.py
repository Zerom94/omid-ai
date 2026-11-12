import os
from flask import Flask, request, render_template, redirect, url_for, g, flash
import sqlite3
from db import init_db

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Insecure hardcoded key

DATABASE = os.path.join(app.root_path, 'vuln.db')

def get_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if not request.cookies.get('username'):
        return redirect(url_for('login'))
    username = request.cookies.get('username')
    return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Vulnerable to SQL injection
        db = get_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = db.execute(query)
        user = cur.fetchone()
        if user:
            resp = redirect(url_for('index'))
            resp.set_cookie('username', username)  # Insecure cookie handling
            return resp
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    db = get_connection()
    # Vulnerable to SQL injection
    query = f"SELECT title, content FROM posts WHERE title LIKE '%{q}%'}"
    cur = db.execute(query)
    results = cur.fetchall()
    return render_template('search.html', query=q, results=results)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db(DATABASE)
    app.run(host='0.0.0.0', port=5000, debug=True)
