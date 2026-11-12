import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vulnweb.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        # Insert default users
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        c.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")
        conn.commit()
        conn.close()
