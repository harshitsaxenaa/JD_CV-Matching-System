from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.parser import extract_text
from utils.matcher import match_cvs_to_jd
import os


app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://jd-cv-match-frontend.onrender.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

UPLOAD_FOLDER = 'backend/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))   
    app.run(host='0.0.0.0', port=port)        
