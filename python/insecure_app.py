import sqlite3
import subprocess
import pickle
import hashlib
import random
import requests
import ast
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
    try:
        node = ast.parse(expr, mode="eval")

        def safe_eval(n):
            if isinstance(n, ast.Expression):
                return safe_eval(n.body)
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
                return n.value
            if isinstance(n, ast.Num):
                return n.n
            if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
                left = safe_eval(n.left)
                right = safe_eval(n.right)
                if isinstance(n.op, ast.Add):
                    return left + right
                if isinstance(n.op, ast.Sub):
                    return left - right
                if isinstance(n.op, ast.Mult):
                    return left * right
                if isinstance(n.op, ast.Div):
                    return left / right
                if isinstance(n.op, ast.FloorDiv):
                    return left // right
                if isinstance(n.op, ast.Mod):
                    return left % right
                if isinstance(n.op, ast.Pow):
                    return left ** right
            if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
                operand = safe_eval(n.operand)
                if isinstance(n.op, ast.UAdd):
                    return +operand
                if isinstance(n.op, ast.USub):
                    return -operand
            raise ValueError("Invalid expression")

        result = safe_eval(node)
        return str(result)
    except Exception:
        return "Invalid expression", 400

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
