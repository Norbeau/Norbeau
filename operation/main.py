from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

# ✅ API Key — for local testing only
openai.api_key = "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"

# ✅ Relative path for GitHub/Codespace
VOCAB_INDEX_FILE = "../database/vocabulary/index.txt"

# ====== Helper Functions ======

def load_index():
    if not os.path.exists(VOCAB_INDEX_FILE):
        with open(VOCAB_INDEX_FILE, "w") as f:
            f.write("File name: index.txt\n")
            f.write("Word count: 0\n")
            f.write("----------\n")
        return 0, []

    with open(VOCAB_INDEX_FILE, "r") as f:
        lines = f.readlines()
        word_count = int(lines[1].split(":")[1].strip())
        words = [line.strip().split(",")[1].strip() for line in lines[3:]]
        return word_count, words

def add_word_to_index(word, new_index):
    with open(VOCAB_INDEX_FILE, "a") as f:
        f.write(f"{{{new_index}, {word}, difficulty: 100%}}\n")

    with open(VOCAB_INDEX_FILE, "r") as f:
        lines = f.readlines()
    lines[1] = f"Word count: {new_index}\n"
    with open(VOCAB_INDEX_FILE, "w") as f:
        f.writelines(lines)

def ask_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip().lower()

# ====== Routes ======

@app.route("/add_word", methods=["POST"])
def add_word():
    data = request.json
    word = data.get("word", "").strip().lower()

    if not word:
        return jsonify({"message": "No word provided."}), 400

    word_count, words = load_index()

    if word in words:
        return jsonify({"message": "The word already exists in your vocabulary."})

    # Step 1: Is it a French word?
    is_french = ask_chatgpt(f'Is "{word}" a French word, only answer "yes" or "no", do not answer any other things like emojis or punctuations, your answer has to be all lowercase')
    if is_french != "yes":
        return jsonify({"message": "It is not a French word."})

    # Step 2: Is it below CLB level 7?
    is_clb = ask_chatgpt(f'Is "{word}" a regular French word below CLB level 7? only answer "yes" or "no", do not answer any other things like emojis or punctuations, your answer has to be all lowercase')
    if is_clb == "yes":
        new_index = word_count + 1
        add_word_to_index(word, new_index)
        return jsonify({"message": f"The word '{word}' has been added to your vocabulary!"})
    else:
        return jsonify({"message": "The word is beyond CLB level 7, not recommended to learn."})

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})
