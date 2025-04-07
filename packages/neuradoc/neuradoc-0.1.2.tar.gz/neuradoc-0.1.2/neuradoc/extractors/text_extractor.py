"""
Module for extracting text from various document elements.
"""

import logging
import re

logger = logging.getLogger(__name__)


def extract_text_from_element(element, clean=True):
    """
    Extract clean, formatted text from an element.
    
    Args:
        element: Element object to extract text from
        clean (bool): Whether to clean and normalize the text
        
    Returns:
        str: Extracted text
    """
    if not element or not hasattr(element, 'content'):
        return ""
    
    content = element.content
    
    # Return content directly if it's already a string
    if isinstance(content, str):
        text = content
    else:
        # Attempt to get string representation
        text = str(content)
    
    # Clean text if requested
    if clean:
        text = clean_text(text)
    
    return text


def clean_text(text):
    """
    Clean and normalize text.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # Normalize whitespace around punctuation
    text = re.sub(r'\s*([.,;:!?])', r'\1 ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_paragraphs(text):
    """
    Split text into paragraphs.
    
    Args:
        text (str): Text to split
        
    Returns:
        list: List of paragraph strings
    """
    if not text:
        return []
    
    # Split by double newlines (paragraph breaks)
    paragraphs = re.split(r'\n\s*\n', text)
    
    # Clean each paragraph
    return [clean_text(p) for p in paragraphs if clean_text(p)]


def extract_sentences(text):
    """
    Split text into sentences.
    
    Args:
        text (str): Text to split
        
    Returns:
        list: List of sentence strings
    """
    if not text:
        return []
    
    # This is a simple sentence splitter that handles common cases
    # For more accurate sentence splitting, consider using NLTK or spaCy
    sentence_pattern = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
    sentences = sentence_pattern.split(text)
    
    # Clean each sentence
    return [clean_text(s) for s in sentences if clean_text(s)]
