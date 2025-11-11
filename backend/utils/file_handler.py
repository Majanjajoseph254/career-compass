import os
from werkzeug.utils import secure_filename
import uuid

def save_upload(file, upload_folder):
    """Save uploaded file with a secure filename"""
    # Get original file extension
    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1]
    
    # Generate unique filename
    unique_filename = f"{str(uuid.uuid4())}{extension}"
    
    # Create full path
    filepath = os.path.join(upload_folder, unique_filename)
    
    # Save file
    file.save(filepath)
    
    return filepath