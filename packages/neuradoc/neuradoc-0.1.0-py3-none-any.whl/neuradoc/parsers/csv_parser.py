"""
Parser for CSV files.
"""

import logging
import os
from pathlib import Path
import csv

import pandas as pd

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for CSV files."""
    
    def parse(self, file_path):
        """
        Parse a CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            # Detect the delimiter
            delimiter = self._detect_delimiter(file_path)
            
            # Read the CSV file
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.reader(file, delimiter=delimiter)
                rows = list(csv_reader)
            
            # Extract document metadata
            file_stats = os.stat(file_path)
            metadata = {
                'title': Path(file_path).stem,
                'size': file_stats.st_size,
                'created': file_stats.st_ctime,
                'modified': file_stats.st_mtime,
                'row_count': len(rows),
                'delimiter': delimiter,
                'file_path': file_path,
                'file_type': 'csv'
            }
            
            # Extract elements
            elements = []
            
            # Add the CSV data as a table element
            if rows:
                elements.append(Element(
                    element_type=ElementType.TABLE,
                    content=rows,
                    position={'index': 0}
                ))
                
                # Also add a processed version with column names (if the CSV has headers)
                if len(rows) > 1:
                    # Assume first row is header
                    header = rows[0]
                    data = rows[1:]
                    
                    # Create a more structured representation
                    structured_data = {
                        'header': header,
                        'data': data
                    }
                    
                    elements.append(Element(
                        element_type=ElementType.TABLE,
                        content=structured_data,
                        metadata={'structured': True},
                        position={'index': 1}
                    ))
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing CSV file {file_path}: {e}")
            raise
    
    def _detect_delimiter(self, file_path):
        """
        Detect the delimiter used in a CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            str: Detected delimiter
        """
        # Common delimiters to check
        delimiters = [',', ';', '\t', '|']
        
        # Read first few lines of the file
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            sample = file.read(4096)  # Read first 4KB
        
        # Count occurrences of each delimiter
        counts = {delimiter: sample.count(delimiter) for delimiter in delimiters}
        
        # Return the delimiter with maximum occurrences
        max_count = 0
        detected_delimiter = ','  # Default to comma
        
        for delimiter, count in counts.items():
            if count > max_count:
                max_count = count
                detected_delimiter = delimiter
        
        return detected_delimiter
