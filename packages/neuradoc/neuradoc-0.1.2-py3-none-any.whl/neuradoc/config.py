"""
Module for configuration settings and parsing options.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union

logger = logging.getLogger(__name__)


@dataclass
class ParsingConfig:
    """Configuration for document parsing settings."""

    # General parsing options
    extraction_level: str = "full"  # Options: 'minimal', 'standard', 'full', 'custom'
    preserve_formatting: bool = True
    include_metadata: bool = True
    max_content_size: Optional[int] = None  # None for no limit

    # Content specific options
    extract_images: bool = True
    extract_tables: bool = True
    extract_diagrams: bool = True
    extract_code: bool = True
    
    # OCR options
    use_ocr: bool = False
    ocr_languages: List[str] = field(default_factory=lambda: ["eng"])
    ocr_dpi: int = 300
    
    # Table extraction options
    table_detection_confidence: float = 0.7
    max_table_size: Optional[int] = None
    
    # Advanced options
    timeout: int = 300  # seconds
    parallel_processing: bool = False
    chunk_large_files: bool = True
    chunk_size: int = 10 * 1024 * 1024  # 10MB
    custom_options: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and adjust configuration after initialization."""
        self._validate()
    
    def _validate(self):
        """Validate configuration values."""
        valid_extraction_levels = ["minimal", "standard", "full", "custom"]
        if self.extraction_level not in valid_extraction_levels:
            logger.warning(f"Invalid extraction_level: {self.extraction_level}. Defaulting to 'standard'")
            self.extraction_level = "standard"
            
        if self.table_detection_confidence < 0 or self.table_detection_confidence > 1:
            logger.warning(f"Invalid table_detection_confidence: {self.table_detection_confidence}. Must be between 0 and 1. Defaulting to 0.7")
            self.table_detection_confidence = 0.7
    
    def update(self, **kwargs):
        """
        Update configuration values.
        
        Args:
            **kwargs: Configuration values to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning(f"Unknown configuration option: {key}")
                self.custom_options[key] = value
        
        self._validate()
    
    @classmethod
    def from_preset(cls, preset: str) -> 'ParsingConfig':
        """
        Create a configuration from a preset.
        
        Args:
            preset (str): Preset name ('fast', 'balanced', 'thorough', 'ocr', 'tables')
            
        Returns:
            ParsingConfig: Configuration with preset values
        """
        presets = {
            "fast": {
                "extraction_level": "minimal",
                "preserve_formatting": False,
                "extract_images": False,
                "extract_tables": False,
                "extract_diagrams": False,
                "extract_code": True,
                "use_ocr": False,
                "timeout": 60
            },
            "balanced": {
                "extraction_level": "standard",
                "preserve_formatting": True,
                "extract_images": True,
                "extract_tables": True,
                "extract_diagrams": False,
                "extract_code": True,
                "use_ocr": False,
                "timeout": 180
            },
            "thorough": {
                "extraction_level": "full",
                "preserve_formatting": True,
                "extract_images": True,
                "extract_tables": True,
                "extract_diagrams": True,
                "extract_code": True,
                "use_ocr": True,
                "timeout": 600
            },
            "ocr": {
                "extraction_level": "standard",
                "preserve_formatting": True,
                "extract_images": True,
                "extract_tables": True,
                "extract_diagrams": False,
                "extract_code": True,
                "use_ocr": True,
                "ocr_dpi": 400,
                "timeout": 300
            },
            "tables": {
                "extraction_level": "standard",
                "preserve_formatting": True,
                "extract_images": False,
                "extract_tables": True,
                "extract_diagrams": False,
                "extract_code": True,
                "use_ocr": False,
                "table_detection_confidence": 0.6,
                "timeout": 180
            }
        }
        
        if preset not in presets:
            logger.warning(f"Unknown preset: {preset}. Defaulting to 'balanced'")
            preset = "balanced"
        
        config = cls()
        config.update(**presets[preset])
        return config


@dataclass
class OutputConfig:
    """Configuration for document output options."""
    
    # General output options
    output_format: str = "text"  # Options: 'text', 'markdown', 'json', 'html'
    include_metadata: bool = True
    pretty_print: bool = True
    
    # Content specific options
    include_images: bool = True
    include_tables: bool = True
    include_diagrams: bool = True
    include_code: bool = True
    
    # Transformation options
    apply_transformations: bool = False
    summarize: bool = False
    translate: bool = False
    target_language: Optional[str] = None
    
    # Advanced options
    max_output_size: Optional[int] = None  # None for no limit
    custom_options: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and adjust configuration after initialization."""
        self._validate()
    
    def _validate(self):
        """Validate configuration values."""
        valid_formats = ["text", "markdown", "json", "html"]
        if self.output_format not in valid_formats:
            logger.warning(f"Invalid output_format: {self.output_format}. Defaulting to 'text'")
            self.output_format = "text"
            
        if self.translate and not self.target_language:
            logger.warning("Translation requested but no target language specified. Disabling translation.")
            self.translate = False
    
    def update(self, **kwargs):
        """
        Update configuration values.
        
        Args:
            **kwargs: Configuration values to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning(f"Unknown configuration option: {key}")
                self.custom_options[key] = value
        
        self._validate()


def create_parsing_profile(profile_name: str, **kwargs) -> Dict[str, Any]:
    """
    Create a named parsing profile with custom settings.
    
    Args:
        profile_name (str): Name of the profile
        **kwargs: Configuration values to set
        
    Returns:
        dict: Dictionary with parsing and output configurations
    """
    parsing_config = ParsingConfig()
    output_config = OutputConfig()
    
    parsing_keys = set(vars(parsing_config).keys())
    
    # Separate kwargs into parsing and output configs
    for key, value in kwargs.items():
        if key in parsing_keys:
            setattr(parsing_config, key, value)
        else:
            setattr(output_config, key, value)
    
    parsing_config._validate()
    output_config._validate()
    
    return {
        "name": profile_name,
        "parsing_config": parsing_config,
        "output_config": output_config
    }


# Built-in parsing profiles
PARSING_PROFILES = {
    "default": create_parsing_profile(
        "default",
        extraction_level="standard",
        output_format="text"
    ),
    "fast": create_parsing_profile(
        "fast",
        extraction_level="minimal",
        extract_images=False,
        extract_tables=False,
        extract_diagrams=False,
        output_format="text"
    ),
    "detailed": create_parsing_profile(
        "detailed",
        extraction_level="full",
        use_ocr=True,
        output_format="markdown"
    ),
    "llm_ready": create_parsing_profile(
        "llm_ready",
        extraction_level="standard",
        preserve_formatting=True,
        output_format="markdown",
        apply_transformations=True
    ),
    "data_extraction": create_parsing_profile(
        "data_extraction",
        extraction_level="standard",
        extract_tables=True,
        table_detection_confidence=0.6,
        output_format="json"
    )
}


def get_parsing_profile(profile_name: str = "default") -> Dict[str, Union[ParsingConfig, OutputConfig]]:
    """
    Get a parsing profile by name.
    
    Args:
        profile_name (str): Name of the profile
        
    Returns:
        dict: Dictionary with parsing and output configurations
    """
    if profile_name not in PARSING_PROFILES:
        logger.warning(f"Unknown profile: {profile_name}. Defaulting to 'default'")
        profile_name = "default"
    
    return PARSING_PROFILES[profile_name]
