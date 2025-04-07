"""
Package containing parsers for different document formats.
"""

from pathlib import Path
import os
import importlib
import logging

logger = logging.getLogger(__name__)

# Dictionary mapping file extensions to parser modules
PARSER_MAP = {
    '.pdf': 'pdf_parser',
    '.docx': 'docx_parser',
    '.doc': 'docx_parser',  # docx parser can handle .doc in some cases
    '.txt': 'txt_parser',
    '.xlsx': 'xlsx_parser',
    '.xls': 'xlsx_parser',  # xlsx parser can handle .xls in some cases
    '.html': 'html_parser',
    '.htm': 'html_parser',
    '.xml': 'xml_parser',
    '.jpg': 'image_parser',
    '.jpeg': 'image_parser',
    '.png': 'image_parser',
    '.gif': 'image_parser',
    '.pptx': 'pptx_parser',
    '.ppt': 'pptx_parser',  # pptx parser can handle .ppt in some cases
    '.csv': 'csv_parser',
    '.json': 'json_parser',
    '.md': 'markdown_parser',
}


def get_parser_for_file(file_path, explicit_type=None):
    """
    Get appropriate parser for the given file.
    
    Args:
        file_path (str): Path to the document file
        explicit_type (str, optional): Explicitly specified document type
        
    Returns:
        Parser: An instance of the appropriate parser class
        
    Raises:
        ValueError: If no parser is available for the file type
    """
    if explicit_type:
        # If type is explicitly specified, use it
        if explicit_type.startswith('.'):
            ext = explicit_type
        else:
            ext = f'.{explicit_type}'
    else:
        # Otherwise infer from file extension
        ext = Path(file_path).suffix.lower()
    
    if ext not in PARSER_MAP:
        supported = ', '.join(PARSER_MAP.keys())
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: {supported}")
    
    parser_module_name = PARSER_MAP[ext]
    try:
        # Import the appropriate parser module
        module = importlib.import_module(f'neuradoc.parsers.{parser_module_name}')
        # Get the parser class
        parser_class = getattr(module, 'Parser')
        # Return an instance of the parser
        return parser_class()
    except (ImportError, AttributeError) as e:
        logger.error(f"Error loading parser for {ext}: {e}")
        raise ValueError(f"Parser implementation not found for {ext}")


class BaseParser:
    """Base class for all document parsers."""
    
    def __init__(self):
        """Initialize the parser with default options."""
        self.options = {
            'extract_images': True,
            'extract_tables': True,
            'extract_diagrams': True,
            'extract_code': True,
            'use_ocr': False,
            'ocr_languages': ['eng'],
            'ocr_dpi': 300,
            'preserve_formatting': True,
            'table_detection_confidence': 0.7,
            'timeout': 300
        }
    
    def configure(self, **kwargs):
        """
        Configure parser options.
        
        Args:
            **kwargs: Parser options to configure
        """
        for key, value in kwargs.items():
            if key in self.options:
                self.options[key] = value
            else:
                logger.warning(f"Unknown option for {self.__class__.__name__}: {key}")
    
    def parse(self, file_path):
        """
        Parse the document at the given file path.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            dict: Parsed content with metadata
        """
        raise NotImplementedError("Parser must implement the parse method")
    
    def validate_file(self, file_path):
        """
        Validate that the file exists and is accessible.
        
        Args:
            file_path (str): Path to check
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def get_file_metadata(self, file_path):
        """
        Get basic file metadata.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: File metadata
        """
        file_path = Path(file_path)
        
        metadata = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'file_type': file_path.suffix[1:] if file_path.suffix else None,
            'size': file_path.stat().st_size if file_path.exists() else 0,
            'created': file_path.stat().st_ctime if file_path.exists() else None,
            'modified': file_path.stat().st_mtime if file_path.exists() else None,
        }
        
        return metadata
    
    def estimate_processing_requirements(self, file_path):
        """
        Estimate resource requirements for processing the file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: Estimated resource requirements
        """
        metadata = self.get_file_metadata(file_path)
        file_size = metadata['size']
        
        # Default requirements estimation based on file size
        requirements = {
            'memory': max(100 * 1024 * 1024, file_size * 5),  # 100MB or 5x file size
            'time': max(10, file_size / (1024 * 1024) * 2),   # 10s or 2s per MB
            'cpu': 1
        }
        
        return requirements
