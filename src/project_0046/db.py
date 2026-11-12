import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    # Insert a default user (admin/admin) - insecure
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    # Sample posts
    c.execute("INSERT INTO posts (title, content) VALUES ('Hello World', 'This is a test post.')")
    c.execute("INSERT INTO posts (title, content) VALUES ('Vuln Demo', 'Demonstrating XSS <script>alert(1)</script>')")
    conn.commit()
    conn.close()
