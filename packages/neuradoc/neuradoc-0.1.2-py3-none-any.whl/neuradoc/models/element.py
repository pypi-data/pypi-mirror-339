"""
Module defining the element data model for document components.
"""

import logging
from enum import Enum, auto

logger = logging.getLogger(__name__)


class ElementType(Enum):
    """Enumeration of document element types."""
    
    UNKNOWN = auto()
    TEXT = auto()
    HEADING = auto()
    TABLE = auto()
    IMAGE = auto()
    DIAGRAM = auto()
    CODE = auto()
    BULLET_LIST = auto()
    NUMBERED_LIST = auto()
    EQUATION = auto()
    CHART = auto()


class Element:
    """
    Class representing an element extracted from a document.
    """
    
    def __init__(self, element_type=ElementType.UNKNOWN, content=None, metadata=None, position=None):
        """
        Initialize an Element instance.
        
        Args:
            element_type (ElementType): Type of the element
            content: Element content (text, image, table data, etc.)
            metadata (dict, optional): Additional metadata about the element
            position (dict, optional): Position information (page, coordinates, etc.)
        """
        self.element_type = element_type
        self.content = content
        self.metadata = metadata or {}
        self.position = position or {}
    
    def __str__(self):
        """
        Get a string representation of the element.
        
        Returns:
            str: String representation
        """
        type_name = self.element_type.name if hasattr(self.element_type, 'name') else str(self.element_type)
        content_preview = str(self.content)[:50] + '...' if len(str(self.content)) > 50 else str(self.content)
        return f"{type_name}: {content_preview}"
    
    def __repr__(self):
        """
        Get a detailed representation of the element.
        
        Returns:
            str: Detailed representation
        """
        type_name = self.element_type.name if hasattr(self.element_type, 'name') else str(self.element_type)
        return f"Element(type={type_name}, metadata={self.metadata}, position={self.position})"
    
    def to_dict(self):
        """
        Convert the element to a dictionary.
        
        Returns:
            dict: Dictionary representation of the element
        """
        from neuradoc.extractors.text_extractor import extract_text_from_element
        
        element_dict = {
            'type': self.element_type.name if hasattr(self.element_type, 'name') else str(self.element_type),
            'metadata': self.metadata,
            'position': self.position
        }
        
        # Handle content based on type
        if self.element_type in (ElementType.TEXT, ElementType.HEADING, ElementType.CODE):
            element_dict['content'] = extract_text_from_element(self)
        elif self.element_type == ElementType.TABLE:
            element_dict['content'] = self.content
        elif self.element_type in (ElementType.IMAGE, ElementType.DIAGRAM):
            # For non-serializable content like images, just note that it exists
            element_dict['content'] = '[Image data]' if self.element_type == ElementType.IMAGE else '[Diagram data]'
        else:
            # For other types, convert to string if possible
            try:
                element_dict['content'] = str(self.content)
            except Exception:
                element_dict['content'] = '[Complex data]'
        
        return element_dict
