import sqlite3

def init_db():
    conn = sqlite3.connect('vuln.db')
    c = conn.cursor()
    # Create tables
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS posts')
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
    # Insert sample data
    c.execute("INSERT INTO users (username, password) VALUES ('admin','adminpass')")
    c.execute("INSERT INTO users (username, password) VALUES ('user','userpass')")
    c.executemany("INSERT INTO posts (title, content) VALUES (?,?)", [
        ('Hello World', 'This is a public post.'),
        ('Flask Tips', 'Some useful Flask tips.'),
        ('Security', 'Beware of SQL injection!')
    ])
    conn.commit()
    conn.close()
