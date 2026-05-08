import sqlite3

DB_NAME = "users.db"


# ---------------- CREATE DATABASE ----------------

def setup_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            parent_name TEXT NOT NULL,

            parent_email TEXT NOT NULL,

            password TEXT NOT NULL

        )
    """)

    conn.commit()

    conn.close()


# ---------------- REGISTER USER ----------------

def register_user(name, email, parent_name, parent_email, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Check duplicate email
    cursor.execute(
        "SELECT email FROM users WHERE email = ?",
        (email,)
    )

    if cursor.fetchone():

        conn.close()

        return False

    # Insert user
    cursor.execute("""
        INSERT INTO users
        (name, email, parent_name, parent_email, password)

        VALUES (?, ?, ?, ?, ?)
    """, (name, email, parent_name, parent_email, password))

    conn.commit()

    conn.close()

    return True


# ---------------- LOGIN USER ----------------

def get_user(email, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
        AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user