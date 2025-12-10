"""
================================================================================
TheDraftClinic - File Service Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module provides file handling utilities including file validation
and secure file upload functionality.
================================================================================
"""

import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, upload_folder):
    """
    Save an uploaded file to the specified folder with a unique name.
    
    Args:
        file: FileStorage object from Flask request
        upload_folder: Path to the upload directory
        
    Returns:
        str: Unique filename if successful, None if file is invalid
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        return unique_filename
    return None
