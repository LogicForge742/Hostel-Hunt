import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from ..services.cloud_storage_service import S3Service

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
        
        # 2. UPLOAD TO S3 (Persistent Storage)
        file_url = S3Service.upload_file(file, filename, folder='hostel-images')
        
        if file_url:
            # 3. Return the permanent S3 URL to the client
            # The client should then save this URL to the Hostel model in the database.
            return jsonify({"url": file_url}), 200
        else:
            return jsonify({"message": "Failed to upload file to cloud storage"}), 500
    
    return jsonify({"message": "File type not allowed"}), 400