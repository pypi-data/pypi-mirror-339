"""
NeuraDoc: Document parsing and transformation library for LLM-ready data.
"""

__version__ = "0.1.2"

from neuradoc.models.document import Document
from neuradoc.models.element import Element, ElementType


def load_document(file_path, doc_type=None, options=None):
    """
    Load and parse a document from the given file path.
    
    Args:
        file_path (str): Path to the document file
        doc_type (str, optional): Document type to explicitly specify format.
                                 If None, will be inferred from file extension.
        options (dict, optional): Parsing options to customize extraction behavior.
    
    Returns:
        Document: A parsed Document object containing all extracted elements
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported
    """
    from neuradoc.models.document import Document
    return Document.from_file(file_path, doc_type, options)


def analyze_document(file_path, profile=None, config=None, output_format=None, output_file=None):
    """
    Analyze a document with advanced parsing and transformation options.
    
    Args:
        file_path (str): Path to the document file
        profile (str, optional): Predefined parsing profile ('default', 'fast', 'detailed', 'llm_ready', 'data_extraction')
        config (dict, optional): Custom configuration options
        output_format (str, optional): Override the output format ('text', 'markdown', 'json', 'html')
        output_file (str, optional): Path to save the transformed output
        
    Returns:
        dict: Analysis results including document summary and transformed content
    """
    from neuradoc.analyzer import analyze_document as _analyze_doc
    return _analyze_doc(file_path, profile, config, output_format, output_file)


def batch_process(file_paths, output_dir=None, profile=None, config=None):
    """
    Process multiple documents in batch mode.
    
    Args:
        file_paths (list): List of file paths to process
        output_dir (str, optional): Directory to save results
        profile (str, optional): Parsing profile to use for all documents
        config (dict, optional): Custom configuration options
        
    Returns:
        list: Processing results for each file
    """
    from neuradoc.analyzer import DocumentAnalyzer
    analyzer = DocumentAnalyzer(config=config, profile=profile)
    return analyzer.batch_process_files(file_paths, output_dir)


def get_available_profiles():
    """
    Get a list of available parsing profiles with descriptions.
    
    Returns:
        dict: Available profiles with descriptions
    """
    from neuradoc.config import PARSING_PROFILES
    
    profiles = {}
    for name, profile in PARSING_PROFILES.items():
        profiles[name] = {
            "extraction_level": profile["parsing_config"].extraction_level,
            "output_format": profile["output_config"].output_format,
            "description": _get_profile_description(name)
        }
    
    return profiles


def _get_profile_description(profile_name):
    """Get description for a parsing profile."""
    descriptions = {
        "default": "Balanced parsing with standard extraction level and text output format.",
        "fast": "Minimal extraction focused on text content only, optimized for speed.",
        "detailed": "Full extraction including OCR and advanced element classification, with markdown output.",
        "llm_ready": "Standard extraction with formatting preserved, optimized for use with LLMs.",
        "data_extraction": "Focus on extracting structured data like tables with json output format."
    }
    
    return descriptions.get(profile_name, "Custom profile.")
