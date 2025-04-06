"""
Parser for PDF documents.
"""

import logging
import io
import os
from pathlib import Path

from PyPDF2 import PdfReader
import pdf2image
import numpy as np

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType
from neuradoc.utils.ocr import extract_text_from_image
from neuradoc.extractors.table_extractor import extract_tables_from_pdf
from neuradoc.extractors.image_extractor import extract_images_from_pdf

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for PDF documents."""
    
    def parse(self, file_path):
        """
        Parse a PDF document.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            logger.info(f"Parsing PDF with {num_pages} pages")
            
            metadata = {
                'title': reader.metadata.title if reader.metadata and reader.metadata.title else Path(file_path).stem,
                'author': reader.metadata.author if reader.metadata and reader.metadata.author else None,
                'subject': reader.metadata.subject if reader.metadata and reader.metadata.subject else None,
                'creator': reader.metadata.creator if reader.metadata and reader.metadata.creator else None,
                'producer': reader.metadata.producer if reader.metadata and reader.metadata.producer else None,
                'num_pages': num_pages,
                'file_path': file_path,
                'file_type': 'pdf'
            }
            
            # Extract elements
            elements = []
            
            # Extract and process each page
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                
                # Extract raw text from PDF
                text = page.extract_text()
                if text and text.strip():
                    elements.append(Element(
                        element_type=ElementType.TEXT,
                        content=text,
                        page=page_num + 1,
                        position={'page': page_num + 1}
                    ))
                
                # Extract tables using Camelot/Tabula
                tables = extract_tables_from_pdf(file_path, page_num + 1)
                for i, table in enumerate(tables):
                    elements.append(Element(
                        element_type=ElementType.TABLE,
                        content=table,
                        page=page_num + 1,
                        position={'page': page_num + 1, 'index': i}
                    ))
                
                # Extract images
                images = extract_images_from_pdf(file_path, page_num + 1)
                for i, img_data in enumerate(images):
                    img, bbox = img_data
                    # Detect if image is a diagram
                    is_diagram = self._detect_if_diagram(img)
                    element_type = ElementType.DIAGRAM if is_diagram else ElementType.IMAGE
                    
                    elements.append(Element(
                        element_type=element_type,
                        content=img,
                        page=page_num + 1,
                        position={'page': page_num + 1, 'bbox': bbox}
                    ))
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
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
