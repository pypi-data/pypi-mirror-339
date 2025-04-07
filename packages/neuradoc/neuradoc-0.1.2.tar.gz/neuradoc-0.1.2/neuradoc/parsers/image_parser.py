"""
Parser for image files.
"""

import logging
import os
from pathlib import Path

from PIL import Image
import numpy as np

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType
from neuradoc.utils.ocr import extract_text_from_image

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for image files."""
    
    def parse(self, file_path):
        """
        Parse an image file.
        
        Args:
            file_path (str): Path to the image file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            # Open the image
            img = Image.open(file_path)
            
            # Extract image metadata
            metadata = {
                'title': Path(file_path).stem,
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'file_path': file_path,
                'file_type': 'image'
            }
            
            # Try to extract EXIF data if available
            exif_data = {}
            if hasattr(img, '_getexif') and img._getexif():
                for tag, value in img._getexif().items():
                    if isinstance(value, (str, int, float)):
                        exif_data[str(tag)] = value
            
            if exif_data:
                metadata['exif'] = exif_data
            
            # Extract elements
            elements = []
            
            # Store the image itself as an element
            elements.append(Element(
                element_type=ElementType.IMAGE,
                content=img,
                position={'index': 0}
            ))
            
            # Check if this is a diagram or contains text
            is_diagram = self._detect_if_diagram(img)
            if is_diagram:
                elements.append(Element(
                    element_type=ElementType.DIAGRAM,
                    content=img,
                    position={'index': 1}
                ))
            
            # Extract text using OCR
            extracted_text = extract_text_from_image(img)
            if extracted_text and extracted_text.strip():
                elements.append(Element(
                    element_type=ElementType.TEXT,
                    content=extracted_text,
                    metadata={'source': 'ocr'},
                    position={'index': 2}
                ))
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing image file {file_path}: {e}")
            raise
    
    def _detect_if_diagram(self, image):
        """
        Heuristic to detect if an image is likely a diagram.
        
        Args:
            image: PIL Image object
            
        Returns:
            bool: True if likely a diagram, False otherwise
        """
        try:
            # Convert to numpy array for analysis
            img_array = np.array(image)
            
            # Simple heuristic: diagrams tend to have fewer unique colors
            # and more uniform color distribution
            if len(img_array.shape) == 3:  # Color image
                unique_colors = np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0)
                # If it has relatively few colors and isn't grayscale, it might be a diagram
                if 5 <= len(unique_colors) <= 50:
                    return True
            
            # More sophisticated diagram detection could be added here
            
            return False
        except Exception as e:
            logger.warning(f"Error in diagram detection: {e}")
            return False
