import sqlite3

def get_connection():
    conn = sqlite3.connect('vulnweb.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, secret TEXT)')
    cur.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, secret) VALUES ('admin', 'flag{example_secret}')")
        cur.execute("INSERT INTO users (username, secret) VALUES ('guest', 'no_secret')")
    conn.commit()
    conn.close()

def query_user(username):
    conn = get_connection()
    cur = conn.cursor()
    # Vulnerable raw SQL query (SQL injection)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

# Initialize the database when the module is imported
init_db()
