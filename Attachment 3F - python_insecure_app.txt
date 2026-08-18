import sqlite3
import subprocess
import pickle
import hashlib
import random
import requests
from flask import Flask, request, make_response

app = Flask(__name__)
DB_PATH = "users.db"

ADMIN_USER = "admin"
ADMIN_PASS = "P@ssw0rd!"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)")
    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username") or ""
    password = request.form.get("password") or ""
    password_hash = hashlib.md5((password + "salt").encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"SELECT id FROM users WHERE username = '{username}' AND password_hash = '{password_hash}'"
    rows = cur.execute(query).fetchall()
    conn.close()
    if rows:
        resp = make_response("Logged in")
        resp.set_cookie("session", "tok_" + str(random.randint(0, 999999)))
        return resp, 200
    return "Invalid", 401

@app.route("/exec")
def exec_cmd():
    cmd = request.args.get("cmd", "echo hello")
    out = subprocess.check_output(cmd, shell=True)
    return out

@app.route("/config")
def config():
    data = request.args.get("data", "")
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

@app.route("/remote")
def remote():
    url = request.args.get("url", "https://example.com")
    r = requests.get(url, verify=False, timeout=2)
    return r.text

@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+2")
    result = eval(expr)
    return str(result)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
