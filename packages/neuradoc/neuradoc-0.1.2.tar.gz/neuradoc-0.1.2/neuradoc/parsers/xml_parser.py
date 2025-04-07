"""
Parser for XML documents.
"""

import logging
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for XML documents."""
    
    def parse(self, file_path):
        """
        Parse an XML file.
        
        Args:
            file_path (str): Path to the XML file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract document metadata
            metadata = {
                'title': Path(file_path).stem,
                'root_tag': root.tag,
                'file_path': file_path,
                'file_type': 'xml'
            }
            
            # Extract namespaces info
            namespaces = {}
            for match in re.finditer(r'xmlns:(\w+)=["\'](.*?)["\']', open(file_path, 'r').read()):
                prefix, uri = match.groups()
                namespaces[prefix] = uri
            
            if namespaces:
                metadata['namespaces'] = namespaces
            
            # Extract elements
            elements = []
            
            # Convert XML structure to text representation
            self._process_element(root, elements)
            
            # Check if this is an SVG
            if root.tag.endswith('svg') or (root.tag.find('}svg') != -1):
                # This is an SVG file, likely a diagram
                with open(file_path, 'r') as f:
                    svg_content = f.read()
                
                elements.append(Element(
                    element_type=ElementType.DIAGRAM,
                    content=svg_content,
                    position={'index': 0}
                ))
            
            # Look for table-like structures
            self._extract_table_structures(root, elements)
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing XML file {file_path}: {e}")
            raise
    
    def _process_element(self, element, elements, path='', index=0):
        """
        Process an XML element and its children.
        
        Args:
            element: XML element
            elements: List to append extracted elements to
            path: Current element path
            index: Current position index
            
        Returns:
            int: Next available position index
        """
        # Build current path
        current_path = f"{path}/{element.tag}" if path else element.tag
        
        # Get all text in this element (including text from children)
        element_text = "".join(element.itertext()).strip()
        
        # If there's text content, add it as a text element
        if element_text:
            elements.append(Element(
                element_type=ElementType.TEXT,
                content=element_text,
                metadata={'path': current_path},
                position={'path': current_path, 'index': index}
            ))
            index += 1
        
        # Recursively process child elements
        for child in element:
            index = self._process_element(child, elements, current_path, index)
        
        return index
    
    def _extract_table_structures(self, root, elements):
        """
        Look for table-like structures in the XML.
        
        Args:
            root: Root XML element
            elements: List to append extracted elements to
        """
        # Look for common table patterns in XML
        # Example pattern: repeated elements with identical child structure
        
        # Check direct children of root
        children = list(root)
        
        # If we have multiple children with the same tag, they might form a table
        if len(children) > 1:
            tag_counts = {}
            for child in children:
                tag_counts[child.tag] = tag_counts.get(child.tag, 0) + 1
            
            for tag, count in tag_counts.items():
                # If we have multiple elements with the same tag, analyze their structure
                if count > 1:
                    rows = []
                    
                    # Get all elements with this tag
                    elements_with_tag = [e for e in children if e.tag == tag]
                    
                    # Check the first element to determine the structure
                    first_element = elements_with_tag[0]
                    first_child_tags = [child.tag for child in first_element]
                    
                    # Only continue if the first element has children
                    if first_child_tags:
                        # Check if all elements have the same structure
                        consistent_structure = True
                        for element in elements_with_tag[1:]:
                            if [child.tag for child in element] != first_child_tags:
                                consistent_structure = False
                                break
                        
                        if consistent_structure:
                            # This looks like a table structure
                            # First row is headers
                            headers = first_child_tags
                            rows.append(headers)
                            
                            # Each element becomes a row
                            for element in elements_with_tag:
                                row = []
                                for header in headers:
                                    child_element = element.find(f"./{header}")
                                    if child_element is not None:
                                        row.append("".join(child_element.itertext()).strip())
                                    else:
                                        row.append("")
                                rows.append(row)
                            
                            if len(rows) > 1:  # Only add non-empty tables
                                elements.append(Element(
                                    element_type=ElementType.TABLE,
                                    content=rows,
                                    metadata={'tag': tag},
                                    position={'tag': tag}
                                ))
