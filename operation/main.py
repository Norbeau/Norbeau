from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all origins and methods (for local/frontend testing)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

# Relative path for local environment
MEMBER_FILE = "../database/member_list.txt"

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
                members[username] = password
    return members

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    members = read_members()

    if username not in members:
        return jsonify({"status": "error", "message": "The username does not exist."})
    if members[username] != password:
        return jsonify({"status": "error", "message": "The password is wrong."})

    return jsonify({"status": "success", "message": f"Welcome to Norbeau, {username}!"})

# ✅ Local test route
@app.route("/ping", methods=["GET", "OPTIONS"])
def ping():
    return jsonify({"status": "ok", "message": "CORS is working"})
