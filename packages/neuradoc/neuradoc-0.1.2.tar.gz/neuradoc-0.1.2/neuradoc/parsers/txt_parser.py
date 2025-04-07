"""
Parser for plain text files.
"""

import logging
import os
from pathlib import Path

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for plain text files."""
    
    def parse(self, file_path):
        """
        Parse a text file.
        
        Args:
            file_path (str): Path to the text file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
            content = None
            
            # Try different encodings
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise ValueError(f"Could not decode text file with any of the tried encodings: {encodings}")
            
            # Get metadata from file stats
            file_stats = os.stat(file_path)
            
            metadata = {
                'title': Path(file_path).stem,
                'size': file_stats.st_size,
                'created': file_stats.st_ctime,
                'modified': file_stats.st_mtime,
                'file_path': file_path,
                'file_type': 'txt'
            }
            
            # Break text into paragraphs
            paragraphs = [p for p in content.split('\n\n') if p.strip()]
            
            elements = []
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    elements.append(Element(
                        element_type=ElementType.TEXT,
                        content=paragraph,
                        position={'index': i}
                    ))
            
            # Handle special sections like tables
            # (Simple ASCII tables can be detected by looking for patterns of spaces and pipes)
            elements = self._detect_and_process_tables(elements)
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing text file {file_path}: {e}")
            raise
    
    def _detect_and_process_tables(self, elements):
        """
        Detect and process ASCII tables in text elements.
        
        Args:
            elements (list): List of Element objects
            
        Returns:
            list: Updated list of elements with tables properly classified
        """
        processed_elements = []
        
        for element in elements:
            if element.element_type == ElementType.TEXT:
                text = element.content
                
                # Check for table patterns (looking for aligned rows with pipes or multiple spaces)
                lines = text.strip().split('\n')
                if len(lines) > 2:
                    # Check if it looks like a table with separator lines and consistent spacing
                    separator_pattern = any(line.count('-') > len(line) * 0.6 for line in lines)
                    pipe_pattern = all('|' in line for line in lines) or all('+' in line for line in lines)
                    
                    consistent_spaces = False
                    if len(lines) > 3:
                        # Check for consistent spacing that might indicate columns
                        space_positions = [
                            [i for i, char in enumerate(line) if char == ' ' and i > 0 and i < len(line)-1 and line[i-1] != ' ' and line[i+1] != ' ']
                            for line in lines
                        ]
                        if space_positions and all(space_positions) and len(set(tuple(sorted(pos)) for pos in space_positions)) <= 3:
                            consistent_spaces = True
                    
                    if (separator_pattern and pipe_pattern) or (pipe_pattern) or consistent_spaces:
                        # This looks like a table, so parse it
                        table_data = []
                        for line in lines:
                            if line.strip() and not all(c in '+-=' for c in line.strip()):
                                if '|' in line:
                                    # Split by pipe
                                    row = [cell.strip() for cell in line.split('|')]
                                    # Remove empty cells at beginning/end if the line started/ended with a pipe
                                    if not row[0]:
                                        row = row[1:]
                                    if row and not row[-1]:
                                        row = row[:-1]
                                else:
                                    # Try to split by consistent spaces
                                    row = []
                                    current_word = ""
                                    for char in line:
                                        if char == ' ' and len(current_word) > 0:
                                            row.append(current_word)
                                            current_word = ""
                                            # Skip consecutive spaces
                                            while char == ' ':
                                                char = ''
                                        else:
                                            current_word += char
                                    if current_word:
                                        row.append(current_word)
                                
                                if row:
                                    table_data.append(row)
                        
                        if table_data and len(table_data) > 1:
                            # Create a table element
                            processed_elements.append(Element(
                                element_type=ElementType.TABLE,
                                content=table_data,
                                position=element.position
                            ))
                            continue
            
            # If we didn't convert to a table, keep the original element
            processed_elements.append(element)
        
        return processed_elements
