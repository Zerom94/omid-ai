# vulnweb

A deliberately vulnerable Flask web application used for security training and demonstration.

## Features
- Simple SQLite backend.
- `/login` endpoint vulnerable to SQL injection (string‑formatted query).
- Pre‑populated users:
  - `admin` / `admin123`
  - `user` / `userpass`

## Setup
bash
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python app.py


Visit `http://127.0.0.1:5000/` in your browser.
