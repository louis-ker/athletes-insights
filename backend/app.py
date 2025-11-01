import os
import re
import json

from ragflow_client import ask_ragflow
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route("/api/ask", methods=["POST"])
# def ask():
#     data = request.get_json()
#     question = data.get("question")
#     session_id = data.get("session_id", "default")

#     raw_answer = ask_ragflow(question, session_id)

#     # Extraire le texte et les sources si possible
#     text_part = raw_answer.split("📄 Source")[0].strip()
#     sources_match = re.search(r"📄 Source\s*:\s*(\[.*\])", raw_answer, re.S)

#     sources = []
#     if sources_match:
#         try:
#             sources = json.loads(sources_match.group(1))
#         except Exception:
#             pass

#     return jsonify({
#         "answer": text_part,
#         "sources": sources
#     })

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    session_id = data.get("session_id", "default")

    result = ask_ragflow(question, session_id)
    return jsonify(result)


@app.route("/api/hello", methods=["GET"])
def hello():
    return {"message": "Hello from Flask!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=True)
