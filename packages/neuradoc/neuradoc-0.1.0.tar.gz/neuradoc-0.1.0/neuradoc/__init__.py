"""
NeuraDoc: Document parsing and transformation library for LLM-ready data.
"""

__version__ = '0.1.0'

from neuradoc.models.document import Document
from neuradoc.models.element import Element, ElementType


def load_document(file_path, doc_type=None):
    """
    Load and parse a document from the given file path.
    
    Args:
        file_path (str): Path to the document file
        doc_type (str, optional): Document type to explicitly specify format.
                                 If None, will be inferred from file extension.
    
    Returns:
        Document: A parsed Document object containing all extracted elements
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported
    """
    from neuradoc.models.document import Document
    return Document.from_file(file_path, doc_type)
