"""
Module for transforming document elements into LLM-ready formats.
"""

import logging
import json
import re
from pathlib import Path

import numpy as np
try:
    import torch
    from transformers import AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from neuradoc.models.element import ElementType
from neuradoc.extractors.text_extractor import extract_text_from_element, clean_text
from neuradoc.extractors.table_extractor import table_to_markdown

logger = logging.getLogger(__name__)


class LLMTransformer:
    """Transformer for converting document elements to LLM-ready formats."""
    
    def __init__(self, model_name=None):
        """
        Initialize the transformer.
        
        Args:
            model_name (str, optional): Name of the tokenizer model to use
        """
        self.tokenizer = None
        
        # Try to load a tokenizer if available
        if TRANSFORMERS_AVAILABLE and model_name:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                logger.info(f"Loaded tokenizer: {model_name}")
            except Exception as e:
                logger.warning(f"Failed to load tokenizer {model_name}: {e}")
    
    def transform_document(self, document, output_format='text', include_metadata=True):
        """
        Transform a document into an LLM-ready format.
        
        Args:
            document: Document object to transform
            output_format (str): Output format ('text', 'markdown', 'json')
            include_metadata (bool): Whether to include document metadata
            
        Returns:
            str or dict: Transformed document
        """
        if output_format == 'text':
            return self.to_text(document, include_metadata)
        elif output_format == 'markdown':
            return self.to_markdown(document, include_metadata)
        elif output_format == 'json':
            return self.to_json(document, include_metadata)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def to_text(self, document, include_metadata=True):
        """
        Convert document to plain text format.
        
        Args:
            document: Document object
            include_metadata (bool): Whether to include document metadata
            
        Returns:
            str: Plain text representation of the document
        """
        text_parts = []
        
        # Add metadata section if requested
        if include_metadata and document.metadata:
            text_parts.append("DOCUMENT METADATA:")
            for key, value in document.metadata.items():
                if key and value:
                    text_parts.append(f"{key}: {value}")
            text_parts.append("")  # Empty line after metadata
        
        # Process elements by type
        if document.elements:
            for i, element in enumerate(document.elements):
                # Add element type as a header
                element_type = element.element_type.name if hasattr(element.element_type, 'name') else str(element.element_type)
                text_parts.append(f"[{element_type}]")
                
                # Process based on element type
                if element.element_type == ElementType.TEXT or element.element_type == ElementType.HEADING:
                    text_parts.append(extract_text_from_element(element))
                
                elif element.element_type == ElementType.TABLE:
                    # For plain text, convert table to a simple text representation
                    text_parts.append(self._table_to_text(element.content))
                
                elif element.element_type == ElementType.IMAGE:
                    # For images, add a placeholder with any alt text or description
                    alt_text = element.metadata.get('alt', '') if element.metadata else ''
                    description = f" - {alt_text}" if alt_text else ""
                    text_parts.append(f"[Image{description}]")
                
                elif element.element_type == ElementType.DIAGRAM:
                    # For diagrams, add a descriptive placeholder
                    diagram_type = element.metadata.get('diagram_type', 'diagram') if element.metadata else 'diagram'
                    text_parts.append(f"[{diagram_type.capitalize()}]")
                
                text_parts.append("")  # Empty line between elements
        
        return "\n".join(text_parts)
    
    def to_markdown(self, document, include_metadata=True):
        """
        Convert document to Markdown format.
        
        Args:
            document: Document object
            include_metadata (bool): Whether to include document metadata
            
        Returns:
            str: Markdown representation of the document
        """
        md_parts = []
        
        # Add title if available
        title = document.metadata.get('title', '') if document.metadata else ''
        if title:
            md_parts.append(f"# {title}\n")
        
        # Add metadata section if requested
        if include_metadata and document.metadata:
            md_parts.append("## Document Metadata\n")
            for key, value in document.metadata.items():
                if key and value and key != 'title':  # Skip title as we already included it
                    md_parts.append(f"**{key}**: {value}")
            md_parts.append("")  # Empty line after metadata
        
        # Process elements by type
        if document.elements:
            current_section = None
            
            for element in document.elements:
                element_type = element.element_type
                
                # Start a new section if element type changes
                if element_type != current_section:
                    current_section = element_type
                    section_name = element_type.name.capitalize() if hasattr(element_type, 'name') else str(element_type)
                    md_parts.append(f"## {section_name} Content\n")
                
                # Process based on element type
                if element_type == ElementType.HEADING:
                    level = element.metadata.get('heading_level', 3) if element.metadata else 3
                    heading_text = extract_text_from_element(element)
                    md_parts.append(f"{'#' * level} {heading_text}\n")
                
                elif element_type == ElementType.TEXT:
                    text = extract_text_from_element(element)
                    md_parts.append(f"{text}\n")
                
                elif element_type == ElementType.TABLE:
                    # Convert table to markdown format
                    md_table = table_to_markdown(element.content)
                    md_parts.append(f"{md_table}\n")
                
                elif element_type == ElementType.IMAGE:
                    # For images, add a markdown image reference
                    alt_text = element.metadata.get('alt', 'Image') if element.metadata else 'Image'
                    image_url = element.content if isinstance(element.content, str) else ''
                    
                    if image_url:
                        md_parts.append(f"![{alt_text}]({image_url})\n")
                    else:
                        md_parts.append(f"*[{alt_text}]*\n")
                
                elif element_type == ElementType.DIAGRAM:
                    # For diagrams, add a descriptive placeholder
                    diagram_type = element.metadata.get('diagram_type', 'Diagram') if element.metadata else 'Diagram'
                    md_parts.append(f"*[{diagram_type}]*\n")
                
                elif element_type == ElementType.CODE:
                    # Format code blocks with markdown code fences
                    code = extract_text_from_element(element, clean=False)
                    language = element.metadata.get('language', '') if element.metadata else ''
                    md_parts.append(f"```{language}\n{code}\n```\n")
        
        return "\n".join(md_parts)
    
    def to_json(self, document, include_metadata=True):
        """
        Convert document to JSON format.
        
        Args:
            document: Document object
            include_metadata (bool): Whether to include document metadata
            
        Returns:
            dict: JSON-serializable representation of the document
        """
        result = {}
        
        # Add metadata if requested
        if include_metadata and document.metadata:
            result['metadata'] = document.metadata
        
        # Process elements
        if document.elements:
            result['elements'] = []
            
            for element in document.elements:
                element_dict = {
                    'type': element.element_type.name if hasattr(element.element_type, 'name') else str(element.element_type),
                    'position': element.position
                }
                
                # Add metadata if available
                if element.metadata:
                    element_dict['metadata'] = element.metadata
                
                # Process content based on element type
                if element.element_type == ElementType.TEXT or element.element_type == ElementType.HEADING:
                    element_dict['content'] = extract_text_from_element(element)
                
                elif element.element_type == ElementType.TABLE:
                    # Include table as a list of lists
                    element_dict['content'] = element.content
                
                elif element.element_type == ElementType.IMAGE:
                    # For images, include reference or description
                    if isinstance(element.content, str):
                        element_dict['content'] = element.content
                    else:
                        # If it's an image object, just note the dimensions
                        if hasattr(element.content, 'size'):
                            element_dict['dimensions'] = element.content.size
                        element_dict['content'] = '[Image data]'
                
                elif element.element_type == ElementType.DIAGRAM:
                    # For diagrams, include type information
                    if isinstance(element.content, str):
                        element_dict['content'] = element.content
                    else:
                        element_dict['content'] = '[Diagram data]'
                
                elif element.element_type == ElementType.CODE:
                    element_dict['content'] = extract_text_from_element(element, clean=False)
                
                else:
                    # For other types, convert content to string
                    element_dict['content'] = str(element.content)
                
                result['elements'].append(element_dict)
        
        return result
    
    def tokenize_text(self, text):
        """
        Tokenize text using the loaded tokenizer.
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            list: Tokenized text
        """
        if not self.tokenizer:
            # Simple tokenization if no tokenizer is available
            return text.split()
        
        # Use the HuggingFace tokenizer
        try:
            tokens = self.tokenizer.tokenize(text)
            return tokens
        except Exception as e:
            logger.warning(f"Tokenization failed: {e}")
            # Fallback to simple tokenization
            return text.split()
    
    def _table_to_text(self, table_data):
        """
        Convert a table to plain text format.
        
        Args:
            table_data: Table as a list of lists
            
        Returns:
            str: Text representation of the table
        """
        if not table_data or not isinstance(table_data, list) or not table_data[0]:
            return ""
        
        result = []
        for row in table_data:
            result.append(" | ".join(str(cell) for cell in row))
        
        return "\n".join(result)


def transform_to_context_chunks(document, chunk_size=1000, overlap=100, format='text'):
    """
    Transform a document into context chunks suitable for LLM processing.
    
    Args:
        document: Document object
        chunk_size (int): Maximum chunk size in characters
        overlap (int): Number of characters to overlap between chunks
        format (str): Output format ('text', 'markdown', 'json')
        
    Returns:
        list: List of context chunks
    """
    transformer = LLMTransformer()
    
    # Convert document to the specified format
    if format == 'text':
        full_text = transformer.to_text(document, include_metadata=False)
    elif format == 'markdown':
        full_text = transformer.to_markdown(document, include_metadata=False)
    elif format == 'json':
        # For JSON, we'll create chunks by element
        return _chunk_json_document(transformer.to_json(document, include_metadata=False), chunk_size)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    # Create chunks from text
    return _create_text_chunks(full_text, chunk_size, overlap)


def _create_text_chunks(text, chunk_size, overlap):
    """
    Split text into overlapping chunks.
    
    Args:
        text (str): Text to split
        chunk_size (int): Maximum chunk size
        overlap (int): Overlap size
        
    Returns:
        list: List of text chunks
    """
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        
        # If adding this paragraph would exceed chunk size, finalize the current chunk
        if current_size + paragraph_size > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            
            # Keep some paragraphs for overlap
            overlap_size = 0
            overlap_paragraphs = []
            
            for p in reversed(current_chunk):
                overlap_size += len(p)
                overlap_paragraphs.insert(0, p)
                
                if overlap_size >= overlap:
                    break
            
            # Start new chunk with overlap
            current_chunk = overlap_paragraphs
            current_size = overlap_size
        
        # Add paragraph to current chunk
        current_chunk.append(paragraph)
        current_size += paragraph_size
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def _chunk_json_document(doc_json, chunk_size):
    """
    Split a JSON document into chunks by elements.
    
    Args:
        doc_json (dict): JSON representation of document
        chunk_size (int): Target chunk size
        
    Returns:
        list: List of JSON chunks
    """
    chunks = []
    
    if 'elements' not in doc_json:
        return [doc_json]
    
    current_chunk = {'elements': []}
    current_size = 0
    
    # Add metadata to all chunks if available
    if 'metadata' in doc_json:
        current_chunk['metadata'] = doc_json['metadata']
    
    for element in doc_json['elements']:
        # Estimate element size
        element_size = len(str(element))
        
        # If adding this element would exceed chunk size, finalize the current chunk
        if current_size + element_size > chunk_size and current_chunk['elements']:
            chunks.append(current_chunk)
            current_chunk = {'elements': []}
            current_size = 0
            
            # Add metadata to the new chunk
            if 'metadata' in doc_json:
                current_chunk['metadata'] = doc_json['metadata']
        
        # Add element to current chunk
        current_chunk['elements'].append(element)
        current_size += element_size
    
    # Add the last chunk if it's not empty
    if current_chunk['elements']:
        chunks.append(current_chunk)
    
    return chunks
