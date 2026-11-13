from flask import Flask, request, render_template_string, g
import sqlite3

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
    db = get_db()
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    db.commit()

@app.route('/')
def index():
    return '''
        <h1>VulnWeb</h1>
        <form action="/login" method="GET">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/login')
def login():
    username = request.args.get('username','')
    password = request.args.get('password','')
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor = get_db().execute(query)
    user = cursor.fetchone()
    if user:
        # XSS vulnerability via render_template_string
        return render_template_string(f"<h2>Welcome, {username}!</h2>")
    else:
        return "Invalid credentials"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # SQL injection vulnerability
        db = get_db()
        db.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        db.commit()
        return "User registered"
    return '''
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Register">
        </form>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
