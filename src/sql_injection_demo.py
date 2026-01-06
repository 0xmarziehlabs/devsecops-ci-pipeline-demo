from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/user")
def get_user():
    username = request.args.get("username")  # user-controlled
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ✅ SAFE: Parameterized query (prevents SQL Injection)
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return str(cursor.fetchall())
