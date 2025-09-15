from flask import Flask, request, jsonify
from groq import Groq
import json
import os

# Load your resume
with open("resume.json") as f:
    resume = json.load(f)

# Setup Flask app
app = Flask(__name__)

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    # Build context
    context = f"My Resume: {json.dumps(resume, indent=2)}"
    system_prompt = (
        "You are Sangay Rabten's AI assistant. "
        "Answer as if you are Sangay, using his resume. "
        "If a question is not covered, reply politely and say Sangay is open to learning."
    )

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",  # Groq's recommended model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context}\n\nEmployer: {question}"}
        ]
    )

    return jsonify({"answer": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
