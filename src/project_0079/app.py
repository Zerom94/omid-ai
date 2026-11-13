from flask import Flask, request, render_template, g
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'vuln.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'adminpass')")
        conn.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-key'

    @app.before_first_request
    def setup():
        init_db()

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/search')
    def search():
        # Vulnerable to SQL injection
        q = request.args.get('q', '')
        db = get_db()
        cursor = db.cursor()
        query = f"SELECT username FROM users WHERE username LIKE '%{q}%'}"
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template('search.html', query=q, results=results)

    @app.route('/echo')
    def echo():
        # Vulnerable to reflected XSS
        msg = request.args.get('msg', '')
        return f"<h1>Echo:</h1><p>{msg}</p>"

    return app
