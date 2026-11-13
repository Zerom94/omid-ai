import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app', 'data.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT
)
''')

# Insert a demo user (credentials stored in plain text)
c.execute("INSERT INTO users (username, password, name) VALUES ('admin', 'admin', 'Administrator')")
conn.commit()
conn.close()
print('Database initialized at', DB_PATH)
