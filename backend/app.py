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
response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

result = response.output_text

return jsonify({"result": result})
@app.route("/")
def home():
    return "AI server running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
