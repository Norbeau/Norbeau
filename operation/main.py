from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your key

# ====== Paths ======
MEMBER_LIST = "../database/member_list.txt"
VOCAB_DIR = "../database/vocabulary/"

# ====== Login Route ======
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user_index = None
    with open(MEMBER_LIST, "r") as f:
        for line in f:
            parts = line.strip().strip("{}").split(",")
            if len(parts) >= 3 and parts[1].strip() == username:
                if parts[2].strip() != password:
                    return jsonify({"status": "error", "message": "The password is wrong."})
                user_index = parts[0].strip()
                break

    if user_index is None:
        return jsonify({"status": "error", "message": "The username does not exist."})

    vocab_file = os.path.join(VOCAB_DIR, f"{user_index}.txt")
    if not os.path.exists(vocab_file):
        with open(vocab_file, "w") as f:
            f.write(f"File name: {user_index}.txt\n")
            f.write("Word count: 0\n")
            f.write("----------\n")

    with open(vocab_file, "r") as f:
        lines = f.readlines()
        word_count = int(lines[1].split(":")[1].strip())

    return jsonify({"status": "success", "message": f"Welcome to Norbeau, {username}", "word_count": word_count})

# ====== Add Word Route ======
@app.route("/add_word", methods=["POST"])
def add_word():
    data = request.json
    word = data.get("word", "").strip().lower()
    user_index = data.get("user_index")

    if not word or not user_index:
        return jsonify({"message": "Invalid input."}), 400

    vocab_file = os.path.join(VOCAB_DIR, f"{user_index}.txt")
    if not os.path.exists(vocab_file):
        return jsonify({"message": "Vocabulary file not found."}), 404

    with open(vocab_file, "r") as f:
        lines = f.readlines()
        word_count = int(lines[1].split(":")[1].strip())
        existing_words = [line.strip().split(",")[1].strip() for line in lines[3:]]

    if word in existing_words:
        return jsonify({"message": "The word already exists in your vocabulary."})

    # Step 1: Is it a French word?
    prompt1 = f'Is "{word}" a French word, only answer "yes" or "no", do not answer any other things like emojis or punctuations, your answer has to be all lowercase'
    answer1 = ask_chatgpt(prompt1)
    if answer1 != "yes":
        return jsonify({"message": "It is not a French word."})

    # Step 2: Is it below CLB 7?
    prompt2 = f'Is "{word}" a regular French word below CLB level 7? only answer "yes" or "no", do not answer any other things like emojis or punctuations, your answer has to be all lowercase'
    answer2 = ask_chatgpt(prompt2)
    if answer2 == "yes":
        new_index = word_count + 1
        with open(vocab_file, "a") as f:
            f.write(f"{{{new_index}, {word}, difficulty: 100%}}\n")
        lines[1] = f"Word count: {new_index}\n"
        with open(vocab_file, "w") as f:
            f.writelines(lines)
        return jsonify({"message": f"The word '{word}' has been added to your vocabulary!"})
    else:
        return jsonify({"message": "The word is beyond CLB level 7, not recommended to learn."})

# ====== Helper ======
def ask_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip().lower()

# ====== Ping ======
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})
