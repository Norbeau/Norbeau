from flask import Flask, request, jsonify

app = Flask(__name__)

# Correct absolute path for PythonAnywhere
MEMBER_FILE = "/home/Norbeau/database/member_list.txt"

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
