import sqlite3

def init_db():
    conn = sqlite3.connect('vulnweb.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    c.execute('DROP TABLE IF EXISTS comments')
    c.execute('CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, comment TEXT)')
    conn.commit()
    conn.close()
    print('Database initialized.')

if __name__ == '__main__':
    init_db()
