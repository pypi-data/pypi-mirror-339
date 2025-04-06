"""
Module for custom exceptions used in the neuradoc package.
"""


class NeuradocError(Exception):
    """Base exception for all neuradoc errors."""
    pass


class ParserError(NeuradocError):
    """Exception raised for errors in the parsing process."""
    
    def __init__(self, message, file_path=None, parser_name=None):
        self.file_path = file_path
        self.parser_name = parser_name
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if parser_name:
            detailed_message = f"[{parser_name}] {detailed_message}"
        if file_path:
            detailed_message = f"{detailed_message} (file: {file_path})"
        
        super().__init__(detailed_message)


class ExtractorError(NeuradocError):
    """Exception raised for errors in the extraction process."""
    
    def __init__(self, message, element_type=None):
        self.element_type = element_type
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if element_type:
            detailed_message = f"[{element_type}] {detailed_message}"
        
        super().__init__(detailed_message)


class TransformerError(NeuradocError):
    """Exception raised for errors in the transformation process."""
    
    def __init__(self, message, format=None):
        self.format = format
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if format:
            detailed_message = f"[Format: {format}] {detailed_message}"
        
        super().__init__(detailed_message)


class ElementError(NeuradocError):
    """Exception raised for errors related to document elements."""
    
    def __init__(self, message, element_type=None, position=None):
        self.element_type = element_type
        self.position = position
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if element_type:
            detailed_message = f"[{element_type}] {detailed_message}"
        if position:
            pos_str = ", ".join(f"{k}={v}" for k, v in position.items())
            detailed_message = f"{detailed_message} (position: {pos_str})"
        
        super().__init__(detailed_message)


class DocumentError(NeuradocError):
    """Exception raised for errors related to document operations."""
    
    def __init__(self, message, document=None):
        self.document = document
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if document and hasattr(document, 'metadata') and document.metadata:
            title = document.metadata.get('title', 'Untitled')
            detailed_message = f"[Document: {title}] {detailed_message}"
        
        super().__init__(detailed_message)


class ValidationError(NeuradocError):
    """Exception raised for validation errors."""
    
    def __init__(self, message, field=None, value=None):
        self.field = field
        self.value = value
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if field:
            detailed_message = f"[Field: {field}] {detailed_message}"
        if value is not None:
            detailed_message = f"{detailed_message} (value: {value})"
        
        super().__init__(detailed_message)


class OCRError(NeuradocError):
    """Exception raised for OCR-related errors."""
    
    def __init__(self, message, source=None):
        self.source = source
        self.message = message
        
        # Construct a more detailed error message
        detailed_message = message
        if source:
            detailed_message = f"[OCR Source: {source}] {detailed_message}"
        
        super().__init__(detailed_message)


class UnsupportedFormatError(NeuradocError):
    """Exception raised when a file format is not supported."""
    
    def __init__(self, file_extension, supported_formats=None):
        self.file_extension = file_extension
        self.supported_formats = supported_formats or []
        
        # Construct a detailed error message
        message = f"Unsupported file format: {file_extension}"
        if supported_formats:
            formats_str = ", ".join(supported_formats)
            message = f"{message}. Supported formats: {formats_str}"
        
        super().__init__(message)
