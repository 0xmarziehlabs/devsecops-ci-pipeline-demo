import sqlite3


def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ❌ Vulnerable: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    return cursor.fetchall()
