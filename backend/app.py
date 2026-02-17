from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    answer = data.get("answer", "")

    prompt = f"""
You are an experienced math teacher.
Analyze the student's solution and explain their mistakes simply.

Student answer:
{answer}

Return:
1) What is wrong
2) Why wrong
3) How to fix
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful math teacher."},
            {"role": "user", "content": prompt}
        ]
    )

    return jsonify({
        "result": response.choices[0].message.content
    })

@app.route("/")
def home():
    return "AI server running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
