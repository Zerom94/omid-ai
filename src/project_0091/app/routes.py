import os
import subprocess
import sqlite3
from flask import request, jsonify

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def register_routes(app):
    @app.route('/')
    def index():
        return 'VulnWeb - vulnerable demo'

    @app.route('/search')
    def search():
        # vulnerable to SQL injection
        q = request.args.get('q', '')
        conn = get_db()
        cursor = conn.execute(f"SELECT id, name FROM users WHERE name LIKE '%{q}%'")
        results = [dict(row) for row in cursor.fetchall()]
        return jsonify(results)

    @app.route('/exec')
    def exec_cmd():
        # vulnerable to command injection
        cmd = request.args.get('cmd', '')
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)
        return '<pre>' + result.decode() + '</pre>'

    @app.route('/login', methods=['POST'])
    def login():
        # insecure password handling (plain text)
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        cursor = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            return jsonify({'status': 'success', 'user': dict(user)})
        else:
            return jsonify({'status': 'fail'}), 401

    @app.route('/register', methods=['POST'])
    def register():
        # insecure direct object reference
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return jsonify({'status': 'registered'})
