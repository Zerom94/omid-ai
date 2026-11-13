from flask import Blueprint, request, render_template_string, g, redirect, url_for
import sqlite3

bp = Blueprint('main', __name__)

DATABASE = 'vulnweb.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@bp.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Insecure login (SQL injection)
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = get_db().execute(query)
        user = cur.fetchone()
        if user:
            return f"Welcome, {username}!"
        else:
            return "Invalid credentials", 401
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Reflected XSS
@bp.route('/search')
def search():
    q = request.args.get('q', '')
    return render_template_string(f"<h1>Results for: {q}</h1>")

# Open redirect
@bp.route('/go')
def go():
    url = request.args.get('url', '/')
    return redirect(url)

# Simple page
@bp.route('/')
def index():
    return '''
        <h1>VulnWeb Demo</h1>
        <ul>
            <li><a href="/login">Login (SQLi)</a></li>
            <li><a href="/search?q=test">Search (XSS)</a></li>
            <li><a href="/go?url=https://example.com">Redirect (Open Redirect)</a></li>
        </ul>
    '''
