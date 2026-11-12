import sqlite3
from flask import Flask, request, g, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'vulnweb.db'

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = get_db().execute(query)
        user = cur.fetchone()
        cur.close()
        if user:
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    db = get_db()
    if request.method == 'POST':
        author = request.form['author']
        comment = request.form['comment']
        # Vulnerable to XSS (stored) and SQL injection
        db.execute(f"INSERT INTO comments (author, comment) VALUES ('{author}', '{comment}')")
        db.commit()
        flash('Comment added')
        return redirect(url_for('comment'))
    cur = db.execute('SELECT author, comment FROM comments')
    rows = cur.fetchall()
    cur.close()
    return render_template('comments.html', comments=rows)

if __name__ == '__main__':
    app.run(debug=True)
