import sqlite3

conn = sqlite3.connect('vulnweb.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS users')
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
c.execute("INSERT INTO users (username, password) VALUES ('user', 'pass')")
conn.commit()
conn.close()
print('Database initialized.')
