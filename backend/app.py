from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils.parser import extract_text
from utils.matcher import match_cvs_to_jd
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

UPLOAD_FOLDER = 'backend/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_files():
    jd_file = request.files.get('jd')
    cv_files = request.files.getlist('cvs')
    
    if not jd_file or not cv_files:
        return jsonify({'error': 'Missing JD or CV files'}), 400
    
    print(f"[] Received files: {jd_file.filename}, {[cv.filename for cv in cv_files]}")
    
    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_file.filename)
    jd_file.save(jd_path)
    jd_text = extract_text(jd_path)
    
    cv_texts = []
    for cv_file in cv_files:
        cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_file.filename)
        cv_file.save(cv_path)
        text = extract_text(cv_path)
        cv_texts.append((cv_file.filename, text))
    
    result = match_cvs_to_jd(jd_text, cv_texts)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins for testing
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))   
    app.run(host='0.0.0.0', port=port)
