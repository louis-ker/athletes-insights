from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # autorise les appels du frontend

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Salut depuis le backend Python ! 🐍"})

if __name__ == '__main__':
    app.run(debug=True)