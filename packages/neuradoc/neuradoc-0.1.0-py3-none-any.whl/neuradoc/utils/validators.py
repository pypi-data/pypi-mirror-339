"""
Module for validation utilities.
"""

import logging
import os
from pathlib import Path
import mimetypes

logger = logging.getLogger(__name__)


def validate_file_exists(file_path):
    """
    Validate that a file exists.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if the file exists
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Path exists but is not a file: {file_path}")
    
    return True


def validate_file_format(file_path, allowed_extensions=None):
    """
    Validate that a file is of an allowed format.
    
    Args:
        file_path (str): Path to the file
        allowed_extensions (list, optional): List of allowed file extensions
        
    Returns:
        bool: True if the file format is valid
        
    Raises:
        ValueError: If the file format is not valid
    """
    # If no allowed extensions are specified, accept all
    if not allowed_extensions:
        return True
    
    extension = Path(file_path).suffix.lower()
    
    if extension not in allowed_extensions:
        supported = ', '.join(allowed_extensions)
        raise ValueError(f"Unsupported file format: {extension}. Supported formats: {supported}")
    
    return True


def validate_file_size(file_path, max_size_mb=50):
    """
    Validate that a file is under the maximum size.
    
    Args:
        file_path (str): Path to the file
        max_size_mb (int): Maximum file size in megabytes
        
    Returns:
        bool: True if the file size is valid
        
    Raises:
        ValueError: If the file is too large
    """
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        raise ValueError(f"File too large: {file_size_mb:.2f} MB. Maximum allowed size: {max_size_mb} MB")
    
    return True


def validate_file_readable(file_path):
    """
    Validate that a file is readable.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if the file is readable
        
    Raises:
        PermissionError: If the file is not readable
    """
    try:
        with open(file_path, 'r', errors='ignore'):
            pass
        return True
    except PermissionError:
        raise PermissionError(f"Permission denied: Cannot read file {file_path}")
    except Exception as e:
        logger.warning(f"Error checking file readability: {e}")
        return False


def validate_mime_type(file_path, allowed_mime_types=None):
    """
    Validate that a file has an allowed MIME type.
    
    Args:
        file_path (str): Path to the file
        allowed_mime_types (list, optional): List of allowed MIME types
        
    Returns:
        bool: True if the MIME type is valid
        
    Raises:
        ValueError: If the MIME type is not valid
    """
    # If no allowed MIME types are specified, accept all
    if not allowed_mime_types:
        return True
    
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type is None:
        logger.warning(f"Could not determine MIME type for {file_path}")
        return True
    
    if mime_type not in allowed_mime_types:
        supported = ', '.join(allowed_mime_types)
        raise ValueError(f"Unsupported MIME type: {mime_type}. Supported types: {supported}")
    
    return True


def validate_text_encoding(file_path, encodings=None):
    """
    Validate that a text file can be read with the given encodings.
    
    Args:
        file_path (str): Path to the file
        encodings (list, optional): List of encodings to try
        
    Returns:
        str: The encoding that worked
        
    Raises:
        UnicodeError: If the file cannot be read with any of the encodings
    """
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)  # Read a chunk to check encoding
            return encoding
        except UnicodeDecodeError:
            continue
    
    supported = ', '.join(encodings)
    raise UnicodeError(f"File {file_path} cannot be decoded with any of the encodings: {supported}")
