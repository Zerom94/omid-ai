from flask import Flask, request, g, render_template_string, redirect, url_for
import sqlite3
import db

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('vuln.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db_conn = g.pop('db', None)
    if db_conn is not None:
        db_conn.close()

@app.route('/')
def index():
    return render_template_string("""<h1>Welcome to VulnWeb</h1>
    <a href=\"/login\">Login</a> | <a href=\"/search\">Search</a>""")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vulnerable to SQL injection
        query = f\"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'\"
        cur = get_db().execute(query)
        user = cur.fetchone()
        if user:
            return f\"Hello, {user['username']}! You are logged in.\"
        else:
            return "Invalid credentials"
    return render_template_string("""<form method=\"post\">
        Username: <input name=\"username\"><br>
        Password: <input name=\"password\" type=\"password\"><br>
        <input type=\"submit\" value=\"Login\">
    </form>""")

@app.route('/search')
def search():
    q = request.args.get('q','')
    # Vulnerable to SQL injection
    query = f\"SELECT title, content FROM posts WHERE title LIKE '%{q}%'\"
    cur = get_db().execute(query)
    rows = cur.fetchall()
    result = "<h2>Search results</h2>"
    for row in rows:
        result += f\"<h3>{row['title']}</h3><p>{row['content']}</p>\"
    return result

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
