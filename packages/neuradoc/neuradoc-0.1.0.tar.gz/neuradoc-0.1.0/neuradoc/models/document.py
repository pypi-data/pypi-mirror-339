"""
Module defining the Document class for representing parsed documents.
"""

import logging
import os
from pathlib import Path

from neuradoc.parsers import get_parser_for_file
from neuradoc.models.element import Element, ElementType
from neuradoc.classifiers.element_classifier import reclassify_elements

logger = logging.getLogger(__name__)


class Document:
    """
    Class representing a parsed document with metadata and elements.
    """
    
    def __init__(self, metadata=None, elements=None):
        """
        Initialize a Document instance.
        
        Args:
            metadata (dict, optional): Document metadata
            elements (list, optional): List of document elements
        """
        self.metadata = metadata or {}
        self.elements = elements or []
    
    @classmethod
    def from_file(cls, file_path, doc_type=None):
        """
        Create a Document instance by parsing a file.
        
        Args:
            file_path (str): Path to the document file
            doc_type (str, optional): Document type, if not inferred from extension
            
        Returns:
            Document: Parsed document
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
        """
        # Get appropriate parser for the file
        parser = get_parser_for_file(file_path, doc_type)
        
        # Parse the document
        parsed_data = parser.parse(file_path)
        
        # Create a Document instance
        doc = cls(
            metadata=parsed_data.get('metadata', {}),
            elements=parsed_data.get('elements', [])
        )
        
        # Reclassify elements if needed
        doc.elements = reclassify_elements(doc.elements)
        
        return doc
    
    def save(self, output_path, format='json'):
        """
        Save the document to a file.
        
        Args:
            output_path (str): Path to save the document to
            format (str): Output format ('json', 'text', 'markdown')
            
        Returns:
            bool: True if successful
        """
        from neuradoc.transformers.llm_transformer import LLMTransformer
        
        try:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Transform the document to the desired format
            transformer = LLMTransformer()
            
            if format == 'json':
                import json
                
                # Convert to JSON and save
                doc_json = transformer.to_json(self)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(doc_json, f, indent=2)
            
            elif format == 'text':
                # Convert to text and save
                doc_text = transformer.to_text(self)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(doc_text)
            
            elif format == 'markdown':
                # Convert to markdown and save
                doc_md = transformer.to_markdown(self)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(doc_md)
            
            else:
                raise ValueError(f"Unsupported output format: {format}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error saving document to {output_path}: {e}")
            return False
    
    def to_dict(self):
        """
        Convert the document to a dictionary.
        
        Returns:
            dict: Dictionary representation of the document
        """
        from neuradoc.transformers.llm_transformer import LLMTransformer
        
        transformer = LLMTransformer()
        return transformer.to_json(self)
    
    def __str__(self):
        """
        Get a string representation of the document.
        
        Returns:
            str: String representation
        """
        title = self.metadata.get('title', 'Untitled Document')
        element_count = len(self.elements)
        element_types = set(e.element_type for e in self.elements)
        element_type_names = [t.name if hasattr(t, 'name') else str(t) for t in element_types]
        
        return f"Document: {title} ({element_count} elements, types: {', '.join(element_type_names)})"
    
    def __repr__(self):
        """
        Get a detailed representation of the document.
        
        Returns:
            str: Detailed representation
        """
        return f"Document(metadata={self.metadata}, elements={len(self.elements)})"
    
    def get_elements_by_type(self, element_type):
        """
        Get elements of a specific type.
        
        Args:
            element_type (ElementType): Type of elements to retrieve
            
        Returns:
            list: List of elements with the specified type
        """
        return [e for e in self.elements if e.element_type == element_type]
    
    def get_text_content(self):
        """
        Get all text content from the document.
        
        Returns:
            str: Combined text content
        """
        from neuradoc.extractors.text_extractor import extract_text_from_element
        
        text_elements = self.get_elements_by_type(ElementType.TEXT)
        text_elements.extend(self.get_elements_by_type(ElementType.HEADING))
        
        return "\n\n".join(extract_text_from_element(element) for element in text_elements)
    
    def get_tables(self):
        """
        Get all tables from the document.
        
        Returns:
            list: List of tables
        """
        return [e.content for e in self.get_elements_by_type(ElementType.TABLE)]
    
    def get_images(self):
        """
        Get all images from the document.
        
        Returns:
            list: List of images
        """
        return [e.content for e in self.get_elements_by_type(ElementType.IMAGE)]
