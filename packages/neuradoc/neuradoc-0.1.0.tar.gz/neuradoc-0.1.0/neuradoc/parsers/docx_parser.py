"""
Parser for Microsoft Word documents.
"""

import logging
from pathlib import Path
import io

import docx
from docx.document import Document as DocxDocument
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image

from neuradoc.parsers import BaseParser
from neuradoc.models.element import Element, ElementType

logger = logging.getLogger(__name__)


class Parser(BaseParser):
    """Parser for Microsoft Word documents."""
    
    def parse(self, file_path):
        """
        Parse a Word document.
        
        Args:
            file_path (str): Path to the DOCX file
            
        Returns:
            dict: Parsed content with metadata
        """
        self.validate_file(file_path)
        
        try:
            doc = docx.Document(file_path)
            
            # Extract document metadata
            metadata = {
                'title': self._get_doc_property(doc, 'title') or Path(file_path).stem,
                'author': self._get_doc_property(doc, 'author'),
                'created': self._get_doc_property(doc, 'created'),
                'modified': self._get_doc_property(doc, 'modified'),
                'file_path': file_path,
                'file_type': 'docx'
            }
            
            # Extract elements
            elements = []
            
            # Process the document body
            for i, element in enumerate(self._iter_block_items(doc)):
                if isinstance(element, Paragraph):
                    if element.text.strip():
                        elements.append(Element(
                            element_type=ElementType.TEXT,
                            content=element.text,
                            position={'index': i}
                        ))
                        
                elif isinstance(element, Table):
                    # Process table
                    table_data = []
                    for row in element.rows:
                        row_data = [cell.text for cell in row.cells]
                        table_data.append(row_data)
                    
                    if table_data:
                        elements.append(Element(
                            element_type=ElementType.TABLE,
                            content=table_data,
                            position={'index': i}
                        ))
            
            # Extract images
            for rel_id, rel in doc.part.rels.items():
                if "image" in rel.target_ref:
                    try:
                        image_data = rel.target_part.blob
                        image = Image.open(io.BytesIO(image_data))
                        
                        elements.append(Element(
                            element_type=ElementType.IMAGE,
                            content=image,
                            position={'rel_id': rel_id}
                        ))
                    except Exception as e:
                        logger.warning(f"Could not extract image: {e}")
            
            return {
                'metadata': metadata,
                'elements': elements
            }
            
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {e}")
            raise
    
    def _get_doc_property(self, doc, property_name):
        """
        Get a property from the document core properties if it exists.
        
        Args:
            doc: docx Document object
            property_name: Name of the property to retrieve
            
        Returns:
            The property value or None if not found
        """
        try:
            if doc.core_properties:
                return getattr(doc.core_properties, property_name)
        except (AttributeError, KeyError):
            pass
        return None
    
    def _iter_block_items(self, doc):
        """
        Iterate through all paragraphs and tables in the document.
        
        Args:
            doc: docx Document object
            
        Yields:
            Each paragraph and table in the document
        """
        if not doc.element.body:
            return
            
        for child in doc.element.body:
            if isinstance(child, CT_P):
                yield Paragraph(child, doc)
            elif isinstance(child, CT_Tbl):
                yield Table(child, doc)
