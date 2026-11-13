from flask import Flask, request, g
import sqlite3

DATABASE = "vuln.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')"
    )
    db.commit()

def create_app():
    app = Flask(__name__)

    @app.before_first_request
    def setup():
        init_db()

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        return '''
        <h1>VulnWeb Demo</h1>
        <form action="/login" method="GET">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit" value="Login">
        </form>
        '''

    @app.route("/login")
    def login():
        # Vulnerable to SQL injection
        username = request.args.get("username", "")
        password = request.args.get("password", "")
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor = get_db().execute(query)
        user = cursor.fetchone()
        if user:
            return f"Welcome, {user[1]}!"
        else:
            return "Invalid credentials"

    return app
