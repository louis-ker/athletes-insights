import os
import sys
import shlex
import subprocess
import json

from ragflow_client import ask_ragflow
from flask import Flask, request, jsonify
from flask_cors import CORS
from subprocess import Popen, PIPE

app = Flask(__name__)
CORS(app)

# @app.route("/api/ask", methods=["POST"])
# def ask():
#     data = request.get_json()
#     question = data.get("question")
#     session_id = data.get("session_id", "default")

#     result = ask_ragflow(question, session_id)
#     return jsonify(result)

@app.route("/api/hello", methods=["GET"])
def hello():
    return {"message": "Hello from Flask!"}


# @app.route("/api/run", methods=["POST"])
# def run_script():
#     data = request.json
#     question = data.get("question")

#     result = subprocess.run(
#         ["python", "main.py", "--no-web-search", "-q", question],
#         capture_output=True,
#         text=True,
#         cwd="rag-article-generator"
#     )

#     stdout = result.stdout

#     try:
#         # 🔧 Utiliser rindex pour capter le DERNIER bloc JSON produit
#         start_marker = "===CANVA_JSON_START==="
#         end_marker = "===CANVA_JSON_END==="
#         start = stdout.rindex(start_marker) + len(start_marker)
#         end = stdout.rindex(end_marker)
#         raw_json = stdout[start:end].strip()
#         canva = json.loads(raw_json)
#         return jsonify(canva)

#     except Exception as e:
#         return jsonify({
#             "error": "Impossible d'extraire le JSON",
#             "stdout": stdout,
#             "exception": str(e)
#         }), 500

@app.route("/api/run", methods=["POST"])
def run_script():
    data = request.json
    question = data.get("question")

    result = subprocess.run(
        ["python", "main.py", "--no-web-search", "-q", question],
        capture_output=True,
        text=True,
        cwd="rag-article-generator"
    )

    stdout = result.stdout  # tous les logs ont été basculés vers STDERR, donc ici quasi que le JSON

    start_marker = "===CANVA_JSON_START==="
    end_marker   = "===CANVA_JSON_END==="

    try:
        if start_marker in stdout and end_marker in stdout:
            raw = stdout.split(start_marker)[-1].split(end_marker)[0].strip()
            canva = json.loads(raw)
            return jsonify(canva)

        # Fallback 1 : bloc CLEAN LLM OUTPUT (moins riche, sans graphs)
        if "CLEAN LLM OUTPUT:" in stdout:
            after = stdout.split("CLEAN LLM OUTPUT:", 1)[1]
            # heuristique simple : prendre du premier '{' au dernier '}'
            s = after.find("{")
            e = after.rfind("}")
            if s != -1 and e != -1 and e > s:
                canva = json.loads(after[s:e+1])
                return jsonify(canva)

        # Fallback 2 : dernier JSON valide dans stdout
        import re
        candidates = re.findall(r"\{[\s\S]*\}", stdout)
        for chunk in reversed(candidates):
            try:
                canva = json.loads(chunk)
                return jsonify(canva)
            except Exception:
                continue

        raise ValueError("Aucun JSON exploitable trouvé dans stdout.")

    except Exception as e:
        return jsonify({
            "error": "Impossible d'extraire le JSON",
            "stdout": stdout[-4000:],   # on tronque pour ne pas noyer le front
            "exception": str(e)
        }), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=True)
