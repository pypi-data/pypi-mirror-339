"""
Parser for Markdown files.
"""

import logging
import os
from pathlib import Path
import re

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for Markdown files."""
    
    def parse(self, file_path):
        """
        Parse a Markdown file.
        
        Args:
            file_path (str): Path to the Markdown file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            # Read the Markdown file
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                md_content = file.read()
            
            # Extract document metadata
            file_stats = os.stat(file_path)
            metadata = {
                'title': Path(file_path).stem,
                'size': file_stats.st_size,
                'created': file_stats.st_ctime,
                'modified': file_stats.st_mtime,
                'file_path': file_path,
                'file_type': 'markdown'
            }
            
            # Extract front matter if present (YAML style)
            front_matter = {}
            front_matter_match = re.match(r'---\s+(.*?)\s+---', md_content, re.DOTALL)
            if front_matter_match:
                front_matter_text = front_matter_match.group(1)
                for line in front_matter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        front_matter[key.strip()] = value.strip()
                
                # Remove front matter from content
                md_content = md_content[front_matter_match.end():].strip()
            
            if front_matter:
                metadata['front_matter'] = front_matter
                if 'title' in front_matter:
                    metadata['title'] = front_matter['title']
            
            # Extract elements
            elements = []
            
            # Process headings
            heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
            for match in heading_pattern.finditer(md_content):
                level = len(match.group(1))
                text = match.group(2).strip()
                
                elements.append(Element(
                    element_type=ElementType.TEXT,
                    content=text,
                    metadata={'type': 'heading', 'level': level},
                    position={'index': match.start()}
                ))
            
            # Process code blocks
            code_block_pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
            for match in code_block_pattern.finditer(md_content):
                language = match.group(1)
                code = match.group(2)
                
                elements.append(Element(
                    element_type=ElementType.TEXT,
                    content=code,
                    metadata={'type': 'code', 'language': language},
                    position={'index': match.start()}
                ))
            
            # Process tables
            tables = self._extract_tables(md_content)
            for i, table in enumerate(tables):
                elements.append(Element(
                    element_type=ElementType.TABLE,
                    content=table,
                    position={'index': i}
                ))
            
            # Process paragraphs - text blocks not in headings, code blocks or tables
            # We'll need to remove all the patterns we've already processed
            processed_text = md_content
            # Remove headings
            processed_text = heading_pattern.sub('', processed_text)
            # Remove code blocks
            processed_text = code_block_pattern.sub('', processed_text)
            # Remove tables
            table_pattern = re.compile(r'\|.*\|.*\n\|[-:| ]+\|.*(\n\|.*\|.*)*', re.MULTILINE)
            processed_text = table_pattern.sub('', processed_text)
            
            # Split remaining text into paragraphs
            paragraphs = [p for p in processed_text.split('\n\n') if p.strip()]
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    elements.append(Element(
                        element_type=ElementType.TEXT,
                        content=paragraph,
                        metadata={'type': 'paragraph'},
                        position={'type': 'paragraph', 'index': i}
                    ))
            
            # Process image references
            image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
            for match in image_pattern.finditer(md_content):
                alt_text = match.group(1)
                image_url = match.group(2)
                
                elements.append(Element(
                    element_type=ElementType.IMAGE,
                    content=image_url,
                    metadata={'alt': alt_text},
                    position={'index': match.start()}
                ))
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing Markdown file {file_path}: {e}")
            raise
    
    def _extract_tables(self, md_content):
        """
        Extract tables from markdown content.
        
        Args:
            md_content (str): Markdown content
            
        Returns:
            list: List of tables as lists of lists
        """
        tables = []
        
        # Find all markdown tables
        table_pattern = re.compile(r'\|.*\|.*\n\|[-:| ]+\|.*(\n\|.*\|.*)*', re.MULTILINE)
        for table_match in table_pattern.finditer(md_content):
            table_text = table_match.group(0)
            rows = table_text.strip().split('\n')
            
            # Process each row of the table
            processed_rows = []
            for i, row in enumerate(rows):
                if i == 1:  # Skip the separator row
                    continue
                
                # Split by pipes and strip whitespace
                cells = [cell.strip() for cell in row.split('|')]
                # Remove empty cells at beginning/end
                if cells and not cells[0]:
                    cells = cells[1:]
                if cells and not cells[-1]:
                    cells = cells[:-1]
                
                if cells:  # Only add non-empty rows
                    processed_rows.append(cells)
            
            if len(processed_rows) > 0:  # Only add tables with content
                tables.append(processed_rows)
        
        return tables
