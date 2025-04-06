"""
Parser for JSON files.
"""

import logging
import json
import os
from pathlib import Path

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for JSON files."""
    
    def parse(self, file_path):
        """
        Parse a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            # Extract document metadata
            file_stats = os.stat(file_path)
            metadata = {
                'title': Path(file_path).stem,
                'size': file_stats.st_size,
                'created': file_stats.st_ctime,
                'modified': file_stats.st_mtime,
                'file_path': file_path,
                'file_type': 'json'
            }
            
            # Extract elements
            elements = []
            
            # Convert JSON to a text representation
            json_text = json.dumps(json_data, indent=2)
            elements.append(Element(
                element_type=ElementType.TEXT,
                content=json_text,
                metadata={'format': 'json'},
                position={'index': 0}
            ))
            
            # Look for array data that could be represented as tables
            self._extract_tables_from_json(json_data, elements)
            
            # Look for text content
            self._extract_text_from_json(json_data, elements)
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {e}")
            raise
    
    def _extract_tables_from_json(self, json_data, elements, path='', index=1):
        """
        Extract table-like structures from JSON data.
        
        Args:
            json_data: Parsed JSON data
            elements: List to append extracted elements to
            path: Current JSON path
            index: Current position index
            
        Returns:
            int: Next available position index
        """
        # Check if the JSON is an array of objects with consistent keys
        if isinstance(json_data, list) and len(json_data) > 0 and all(isinstance(item, dict) for item in json_data):
            # Get all unique keys from all objects
            all_keys = set()
            for item in json_data:
                all_keys.update(item.keys())
            
            # Only proceed if we have some keys and more than one row
            if all_keys and len(json_data) > 1:
                # Convert to a table format
                header = list(all_keys)
                rows = [header]
                
                for item in json_data:
                    row = [str(item.get(key, '')) for key in header]
                    rows.append(row)
                
                elements.append(Element(
                    element_type=ElementType.TABLE,
                    content=rows,
                    metadata={'path': path},
                    position={'path': path, 'index': index}
                ))
                index += 1
        
        # Recursively process nested structures
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    index = self._extract_tables_from_json(value, elements, current_path, index)
        
        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                current_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    index = self._extract_tables_from_json(item, elements, current_path, index)
        
        return index
    
    def _extract_text_from_json(self, json_data, elements, path='', index=100):
        """
        Extract textual content from JSON data.
        
        Args:
            json_data: Parsed JSON data
            elements: List to append extracted elements to
            path: Current JSON path
            index: Current position index
            
        Returns:
            int: Next available position index
        """
        if isinstance(json_data, dict):
            # Look for fields that might contain significant text
            text_fields = ['text', 'description', 'content', 'summary', 'body', 'title', 'message']
            
            for field in text_fields:
                if field in json_data and isinstance(json_data[field], str) and len(json_data[field]) > 50:
                    elements.append(Element(
                        element_type=ElementType.TEXT,
                        content=json_data[field],
                        metadata={'path': f"{path}.{field}"},
                        position={'path': f"{path}.{field}", 'index': index}
                    ))
                    index += 1
            
            # Recursively process nested structures
            for key, value in json_data.items():
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    index = self._extract_text_from_json(value, elements, current_path, index)
        
        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                current_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    index = self._extract_text_from_json(item, elements, current_path, index)
                elif isinstance(item, str) and len(item) > 50:
                    elements.append(Element(
                        element_type=ElementType.TEXT,
                        content=item,
                        metadata={'path': current_path},
                        position={'path': current_path, 'index': index}
                    ))
                    index += 1
        
        return index
