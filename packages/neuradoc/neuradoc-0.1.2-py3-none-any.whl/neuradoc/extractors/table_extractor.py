"""
Module for extracting tables from documents.
"""

import logging
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

logger = logging.getLogger(__name__)

# Optional imports for specialized table extraction
try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False


def extract_tables_from_pdf(pdf_path, page_number=None):
    """
    Extract tables from a PDF document.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_number (int, optional): Specific page to extract tables from.
                                    If None, extracts from all pages.
    
    Returns:
        list: List of tables as lists of lists (rows of cells)
    """
    tables = []
    
    # Try different table extraction methods in order of preference
    if CAMELOT_AVAILABLE:
        try:
            # Camelot tends to give the best results for PDFs with tables
            pages = str(page_number) if page_number else "all"
            camelot_tables = camelot.read_pdf(pdf_path, pages=pages, flavor='lattice')
            
            # If no lattice tables found, try stream mode
            if len(camelot_tables) == 0:
                camelot_tables = camelot.read_pdf(pdf_path, pages=pages, flavor='stream')
            
            for table in camelot_tables:
                tables.append(table.data)
            
            if tables:
                return tables
        except Exception as e:
            logger.warning(f"Camelot table extraction failed: {e}")
    
    if TABULA_AVAILABLE:
        try:
            # Tabula is another good option for PDF tables
            page = page_number if page_number else "all"
            tabula_tables = tabula.read_pdf(pdf_path, pages=page, multiple_tables=True)
            
            for df in tabula_tables:
                if not df.empty:
                    # Convert DataFrame to list of lists
                    table_data = [df.columns.tolist()]
                    table_data.extend(df.values.tolist())
                    tables.append(table_data)
            
            if tables:
                return tables
        except Exception as e:
            logger.warning(f"Tabula table extraction failed: {e}")
    
    # If specialized libraries failed or aren't available, try a basic approach
    # This is a placeholder for a very basic extraction
    logger.warning("Using basic table extraction as specialized libraries failed or are unavailable")
    
    # Return empty list if no tables were found
    return tables


def extract_tables_from_image(image):
    """
    Extract tables from an image.
    
    Args:
        image: PIL Image object or path to image file
        
    Returns:
        list: List of tables as lists of lists (rows of cells)
    """
    # This is a placeholder for image-based table extraction
    # In a real implementation, you might use OpenCV or a ML model to detect tables
    
    # For now, return an empty list
    return []


def table_to_markdown(table_data):
    """
    Convert a table to Markdown format.
    
    Args:
        table_data: Table as a list of lists
        
    Returns:
        str: Markdown formatted table
    """
    if not table_data or not isinstance(table_data, list) or not table_data[0]:
        return ""
    
    # Calculate column widths based on content
    col_widths = [0] * len(table_data[0])
    for row in table_data:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build the markdown table
    result = []
    
    # Header row
    header = "| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(table_data[0])) + " |"
    result.append(header)
    
    # Separator row
    separator = "| " + " | ".join("-" * col_widths[i] for i in range(len(col_widths))) + " |"
    result.append(separator)
    
    # Data rows
    for row in table_data[1:]:
        row_str = "| " + " | ".join(str(cell).ljust(min(col_widths[i], 30)) if i < len(col_widths) else "" 
                                   for i, cell in enumerate(row)) + " |"
        result.append(row_str)
    
    return "\n".join(result)


def table_to_dataframe(table_data):
    """
    Convert a table to a pandas DataFrame.
    
    Args:
        table_data: Table as a list of lists
        
    Returns:
        DataFrame: Pandas DataFrame representation of the table
    """
    if not table_data or not isinstance(table_data, list) or not table_data[0]:
        return pd.DataFrame()
    
    headers = table_data[0]
    data = table_data[1:]
    
    # Handle the case where data rows might have fewer columns than header
    max_cols = len(headers)
    normalized_data = []
    for row in data:
        if len(row) < max_cols:
            normalized_data.append(row + [''] * (max_cols - len(row)))
        else:
            normalized_data.append(row[:max_cols])
    
    return pd.DataFrame(normalized_data, columns=headers)
