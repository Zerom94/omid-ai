from flask import Flask, request, render_template, g, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'vuln.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Insert demo user if table empty
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin123'))
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '')
        # Vulnerable SQL query (SQL injection)
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cur = get_db().execute(query)
        user = cur.fetchone()
        cur.close()
        if user:
            return f"Welcome, {user['username']}! Your password is {user['password']}."
        else:
            return "User not found."
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
