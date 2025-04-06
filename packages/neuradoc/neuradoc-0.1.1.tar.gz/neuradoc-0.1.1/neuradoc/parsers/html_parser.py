"""
Parser for HTML documents.
"""

import logging
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
import io

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for HTML documents."""
    
    def parse(self, file_path):
        """
        Parse an HTML document.
        
        Args:
            file_path (str): Path to the HTML file or URL
            
        Returns:
            dict: Parsed content with metadata
        """
        # Check if file_path is a URL
        parsed_url = urlparse(file_path)
        is_url = bool(parsed_url.scheme and parsed_url.netloc)
        
        if is_url:
            try:
                response = requests.get(file_path, timeout=10)
                response.raise_for_status()  # Raise exception for HTTP errors
                html_content = response.text
                document_source = file_path
            except Exception as e:
                logger.error(f"Error fetching HTML from URL {file_path}: {e}")
                raise
        else:
            self.validate_file(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                html_content = file.read()
            document_source = file_path
        
        try:
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract metadata
            metadata = {
                'title': soup.title.text.strip() if soup.title else Path(document_source).stem,
                'file_path': document_source,
                'file_type': 'html'
            }
            
            # Extract metadata from meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name', meta.get('property', ''))
                content = meta.get('content', '')
                if name and content:
                    metadata[f'meta_{name}'] = content
            
            # Extract elements
            elements = []
            
            # Extract main textual content
            # First, remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get all text blocks
            body = soup.body
            if body:
                # Process the document body by tags
                self._process_html_body(body, elements)
            
            # Extract tables
            tables = soup.find_all('table')
            for i, table in enumerate(tables):
                try:
                    # Convert HTML table to list of lists
                    rows = []
                    for tr in table.find_all('tr'):
                        row = []
                        for cell in tr.find_all(['td', 'th']):
                            row.append(cell.get_text(strip=True))
                        if row:  # Add only non-empty rows
                            rows.append(row)
                    
                    if rows:  # Add only non-empty tables
                        elements.append(Element(
                            element_type=ElementType.TABLE,
                            content=rows,
                            position={'index': i}
                        ))
                except Exception as e:
                    logger.warning(f"Error processing table {i}: {e}")
            
            # Extract images
            images = soup.find_all('img')
            for i, img in enumerate(images):
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                if src:
                    # For now, just store the image reference
                    # In a real implementation, we might download and process the image
                    elements.append(Element(
                        element_type=ElementType.IMAGE,
                        content=src,
                        metadata={'alt': alt},
                        position={'index': i}
                    ))
            
            # Extract SVG diagrams
            svgs = soup.find_all('svg')
            for i, svg in enumerate(svgs):
                elements.append(Element(
                    element_type=ElementType.DIAGRAM,
                    content=str(svg),
                    position={'index': i}
                ))
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing HTML {document_source}: {e}")
            raise
    
    def _process_html_body(self, body, elements, current_position=0):
        """
        Process the HTML body and extract text elements.
        
        Args:
            body: BeautifulSoup body tag
            elements: List to append elements to
            current_position: Current position index
            
        Returns:
            int: Next available position index
        """
        # Text-containing tags of interest in approximate order of importance
        important_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'article', 'section', 'div', 'li', 'blockquote']
        
        # Process direct important tags first
        for tag_name in important_tags:
            for tag in body.find_all(tag_name, recursive=False):
                # Extract clean text from this tag
                text = tag.get_text(strip=True, separator=' ')
                if text:
                    element_type = ElementType.TEXT
                    
                    # Special case for headers
                    if tag_name.startswith('h') and len(tag_name) == 2 and tag_name[1].isdigit():
                        heading_level = int(tag_name[1])
                        elements.append(Element(
                            element_type=element_type,
                            content=text,
                            metadata={'tag': tag_name, 'heading_level': heading_level},
                            position={'index': current_position}
                        ))
                    else:
                        elements.append(Element(
                            element_type=element_type,
                            content=text,
                            metadata={'tag': tag_name},
                            position={'index': current_position}
                        ))
                    
                    current_position += 1
                
                # Remove this tag so we don't process it again
                tag.extract()
        
        # Get remaining text that wasn't in the important tags
        remaining_text = body.get_text(strip=True, separator=' ')
        if remaining_text:
            elements.append(Element(
                element_type=ElementType.TEXT,
                content=remaining_text,
                position={'index': current_position}
            ))
            current_position += 1
        
        return current_position
