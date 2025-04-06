"""
Module for Optical Character Recognition (OCR) functionality.
"""

import logging
import os
import tempfile

from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

# Try to import pytesseract
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def extract_text_from_image(image, lang='eng'):
    """
    Extract text from an image using OCR.
    
    Args:
        image: PIL Image object or path to image file
        lang (str): Language code for OCR (default: 'eng')
        
    Returns:
        str: Extracted text
    """
    if not TESSERACT_AVAILABLE:
        logger.warning("pytesseract is not available. OCR functionality is disabled.")
        return ""
    
    try:
        # Load the image if a path is provided
        if isinstance(image, str):
            image = Image.open(image)
        
        # Preprocess the image for better OCR results
        preprocessed_image = preprocess_image_for_ocr(image)
        
        # Perform OCR with pytesseract
        text = pytesseract.image_to_string(preprocessed_image, lang=lang)
        
        return text
    
    except Exception as e:
        logger.error(f"Error performing OCR: {e}")
        return ""


def preprocess_image_for_ocr(image):
    """
    Preprocess an image to improve OCR accuracy.
    
    Args:
        image: PIL Image object
        
    Returns:
        Image: Preprocessed image
    """
    try:
        # Convert to grayscale if it's a color image
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize if the image is very small
        if image.width < 1000 and image.height < 1000:
            # Calculate new dimensions while maintaining aspect ratio
            scale_factor = 1.5
            new_width = int(image.width * scale_factor)
            new_height = int(image.height * scale_factor)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to numpy array for additional processing
        img_array = np.array(image)
        
        # Apply additional preprocessing based on image characteristics
        # (More sophisticated preprocessing could be added here)
        
        # Convert back to PIL Image
        return Image.fromarray(img_array)
    
    except Exception as e:
        logger.warning(f"Error preprocessing image: {e}")
        return image


def ocr_with_layout_analysis(image, lang='eng'):
    """
    Perform OCR with layout analysis to preserve document structure.
    
    Args:
        image: PIL Image object or path to image file
        lang (str): Language code for OCR
        
    Returns:
        dict: Extracted text with layout information
    """
    if not TESSERACT_AVAILABLE:
        logger.warning("pytesseract is not available. OCR layout analysis is disabled.")
        return {"text": ""}
    
    try:
        # Load the image if a path is provided
        if isinstance(image, str):
            image = Image.open(image)
        
        # Preprocess the image
        preprocessed_image = preprocess_image_for_ocr(image)
        
        # Extract text with layout information
        ocr_data = pytesseract.image_to_data(preprocessed_image, lang=lang, output_type=pytesseract.Output.DICT)
        
        # Process OCR data to extract structured information
        result = {
            "text": pytesseract.image_to_string(preprocessed_image, lang=lang),
            "blocks": []
        }
        
        # Group by block number
        blocks = {}
        for i, block_num in enumerate(ocr_data['block_num']):
            if block_num == 0:
                continue
                
            if block_num not in blocks:
                blocks[block_num] = []
            
            if ocr_data['text'][i].strip():
                blocks[block_num].append({
                    'text': ocr_data['text'][i],
                    'conf': ocr_data['conf'][i],
                    'left': ocr_data['left'][i],
                    'top': ocr_data['top'][i],
                    'width': ocr_data['width'][i],
                    'height': ocr_data['height'][i]
                })
        
        # Add blocks to result
        for block_num, words in blocks.items():
            if words:
                block_text = ' '.join(word['text'] for word in words)
                top = min(word['top'] for word in words)
                left = min(word['left'] for word in words)
                
                result['blocks'].append({
                    'text': block_text,
                    'position': {'top': top, 'left': left},
                    'words': words
                })
        
        return result
    
    except Exception as e:
        logger.error(f"Error performing OCR with layout analysis: {e}")
        return {"text": ""}
