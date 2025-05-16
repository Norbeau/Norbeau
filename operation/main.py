from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

# Relative paths for local or GitHub-based use
MEMBER_FILE = "../database/member_list.txt"
VOCAB_DIR = "../database/vocabulary"

def read_members():
    members = {}
    with open(MEMBER_FILE, "r") as file:
        for line in file:
            line = line.strip().strip("{}")
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                index, username, password, *rest = parts
                members[username] = {"id": index, "password": password}
    return members

def ensure_vocab_file(user_id):
    file_path = os.path.join(VOCAB_DIR, f"{user_id}.txt")
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("Word count: 0\n")
            f.write("-------------------\n")
    return file_path

def read_word_count(file_path):
    try:
        with open(file_path, "r") as f:
            line = f.readline().strip()
            if line.startswith("Word count:"):
                return int(line.replace("Word count:", "").strip())
    except:
        pass
    return 0

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    members = read_members()
    if username not in members:
        return jsonify({"status": "error", "message": "The username does not exist."})
    if members[username]["password"] != password:
        return jsonify({"status": "error", "message": "The password is wrong."})

    user_id = members[username]["id"]
    vocab_file = ensure_vocab_file(user_id)
    word_count = read_word_count(vocab_file)

    return jsonify({
        "status": "success",
        "message": f"Welcome to Norbeau, {username}!",
        "word_count": word_count,
        "user_id": user_id
    })

@app.route("/ping", methods=["GET", "OPTIONS"])
def ping():
    return jsonify({"status": "ok", "message": "CORS is working"})
