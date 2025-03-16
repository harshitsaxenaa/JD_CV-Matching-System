from flask import Flask, request, jsonify, send_from_directory
from utils.parser import extract_text
from flask_cors import CORS
from utils.matcher import match_cvs_to_jd
import os

app = Flask(__name__, static_folder=os.path.join(os.path.pardir, 'frontend'), static_url_path='')
CORS(app)

UPLOAD_FOLDER = 'backend/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_files():
    jd_file = request.files['jd']
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_file.filename)
    jd_file.save(jd_path)
    jd_text = extract_text(jd_path)

    cvs = request.files.getlist('cvs')
    results = {}
    for cv_file in cvs:
        cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_file.filename)
        cv_file.save(cv_path)
        cv_text = extract_text(cv_path)
        score = match_cvs_to_jd(jd_text, cv_text)
        results[cv_file.filename] = {"match_score": round(score * 100, 2)}

    return jsonify(results)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "JD-CV Matching Backend is Live "}), 200

if __name__ == '__main__':
    app.run(debug=True)
