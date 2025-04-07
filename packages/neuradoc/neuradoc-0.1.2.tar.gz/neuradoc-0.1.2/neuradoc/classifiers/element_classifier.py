"""
Module for classifying document elements.
"""

import logging
import re
from PIL import Image
import numpy as np

from neuradoc.models.element import ElementType

logger = logging.getLogger(__name__)


class ElementClassifier:
    """Classifier for document elements."""
    
    def __init__(self):
        """Initialize the element classifier."""
        self.features = {}
    
    def classify_element(self, content, metadata=None):
        """
        Classify document element based on content and metadata.
        
        Args:
            content: Element content (text, image, etc.)
            metadata (dict, optional): Additional metadata about the element
            
        Returns:
            ElementType: Classification of the element
        """
        # Extract features
        self._extract_features(content, metadata)
        
        # Classify based on content type
        if isinstance(content, str):
            return self._classify_text()
        elif isinstance(content, Image.Image):
            return self._classify_image()
        elif isinstance(content, list) and content and isinstance(content[0], list):
            return ElementType.TABLE
        else:
            return ElementType.UNKNOWN
    
    def _extract_features(self, content, metadata):
        """
        Extract features from the element content for classification.
        
        Args:
            content: Element content
            metadata (dict): Element metadata
        """
        self.features = {
            'is_text': isinstance(content, str),
            'is_image': isinstance(content, Image.Image),
            'is_table': isinstance(content, list) and content and isinstance(content[0], list),
            'metadata': metadata or {},
        }
        
        # Text-specific features
        if self.features['is_text']:
            text = content
            self.features.update({
                'length': len(text),
                'contains_numbers': bool(re.search(r'\d', text)),
                'contains_special_chars': bool(re.search(r'[^\w\s]', text)),
                'contains_tables': bool(re.search(r'\|.*\|', text)) or 
                                    bool(re.search(r'[+\-]+[+\-]', text)),
                'contains_code': bool(re.search(r'(import|def|function|class|if|return|for)\s', text)) or
                                 bool(re.search(r'[{};]', text)),
                'is_heading': bool(metadata and metadata.get('type') == 'heading'),
                'heading_level': metadata.get('heading_level', 0) if metadata else 0,
                'is_bullet_list': bool(re.search(r'^\s*[\*\-•]\s+', text, re.MULTILINE)),
                'is_numbered_list': bool(re.search(r'^\s*\d+[.)]\s+', text, re.MULTILINE)),
                'line_count': text.count('\n') + 1,
                'avg_line_length': sum(len(line) for line in text.split('\n')) / max(1, text.count('\n') + 1),
            })
        
        # Image-specific features
        if self.features['is_image']:
            image = content
            # Extract basic image features
            self.features.update({
                'image_mode': image.mode,
                'image_size': image.size,
                'image_aspect_ratio': image.size[0] / max(1, image.size[1]),
            })
            
            # Try to determine if it's a diagram
            try:
                img_array = np.array(image)
                if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
                    # Count unique colors for colored images
                    flattened = img_array.reshape(-1, img_array.shape[2])
                    unique_colors = np.unique(flattened, axis=0)
                    self.features['unique_color_count'] = len(unique_colors)
                    
                    # Diagrams often have a limited color palette
                    self.features['likely_diagram'] = 5 <= len(unique_colors) <= 50
                else:
                    # For grayscale images
                    unique_values = np.unique(img_array)
                    self.features['unique_color_count'] = len(unique_values)
                    self.features['likely_diagram'] = 5 <= len(unique_values) <= 20
            except Exception as e:
                logger.warning(f"Error analyzing image: {e}")
                self.features['likely_diagram'] = False
    
    def _classify_text(self):
        """
        Classify text content based on extracted features.
        
        Returns:
            ElementType: Classification of the text element
        """
        # Check for table markers
        if self.features['contains_tables']:
            # This might be a text representation of a table
            return ElementType.TABLE
        
        # Check for code
        if self.features['contains_code'] and not self.features['is_heading']:
            # Lines with programming language constructs are likely code
            if self.features['line_count'] > 1 and '{' in self.features.get('metadata', {}).get('tag', ''):
                return ElementType.CODE
        
        # Check for headings
        if self.features['is_heading'] or self.features['heading_level'] > 0:
            return ElementType.HEADING
        
        # Default to regular text
        return ElementType.TEXT
    
    def _classify_image(self):
        """
        Classify image content based on extracted features.
        
        Returns:
            ElementType: Classification of the image element
        """
        # Check if it's likely a diagram
        if self.features.get('likely_diagram', False):
            return ElementType.DIAGRAM
        
        # Default to image
        return ElementType.IMAGE


def reclassify_elements(elements):
    """
    Reclassify a list of elements based on additional heuristics.
    
    Args:
        elements (list): List of Element objects
        
    Returns:
        list: List of reclassified Element objects
    """
    classifier = ElementClassifier()
    
    for element in elements:
        # Only reclassify if the element doesn't have a specific type already
        if element.element_type == ElementType.UNKNOWN:
            element.element_type = classifier.classify_element(
                element.content, element.metadata
            )
    
    return elements
