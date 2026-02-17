from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# ===== SIMPLE AI LOGIC =====
def analyze_mistake(answer):

    answer = answer.lower()

    if len(answer.strip()) < 5:
        return "Careless mistake", "Your answer is too short — you likely rushed."

    if "because" not in answer and "=>" not in answer:
        return "Logical reasoning mistake", "You gave an answer without explaining reasoning."

    math_symbols = ["=", "+", "-", "*", "/", "^"]
    if not any(sym in answer for sym in math_symbols):
        return "Wrong method selection", "You used explanation but no mathematical method."

    if re.search(r"\d+\s*=\s*\d+\s*\+\s*\d+", answer):
        return "Concept misunderstanding", "You are misunderstanding equality concepts."

    return "Correct reasoning", "Your reasoning structure looks acceptable."


# ===== API =====
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    label, feedback = analyze_mistake(text)

    return jsonify({
        "type": label,
        "feedback": feedback
    })


if __name__ == "__main__":
    app.run(debug=True)
