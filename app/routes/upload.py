import os
import uuid
from flask import Blueprint, request, jsonify, current_app, url_for

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.post("/")
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        # 1. Create a secure, unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # 2. Ensure the upload folder exists
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 3. Save the file
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # 4. Generate the public URL for this file
        # This returns something like http://localhost:5000/static/uploads/abc1234.jpg
        file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        
        return jsonify({"url": file_url}), 200
    
    return jsonify({"message": "File type not allowed"}), 400