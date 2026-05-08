import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT UNIQUE,
                    parent_name TEXT,
                    parent_email TEXT,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

def register_user(name, email, parent_name, parent_email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, parent_name, parent_email, password) VALUES (?, ?, ?, ?, ?)",
              (name, email, parent_name, parent_email, password))
    conn.commit()
    conn.close()

def get_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user
