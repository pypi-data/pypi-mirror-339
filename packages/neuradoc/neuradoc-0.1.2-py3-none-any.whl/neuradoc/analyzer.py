"""
Module for advanced document analysis and optimized parsing.
"""

import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import concurrent.futures

from neuradoc.config import ParsingConfig, OutputConfig, get_parsing_profile
from neuradoc.models.document import Document
from neuradoc.models.element import Element, ElementType
from neuradoc.transformers.llm_transformer import LLMTransformer
from neuradoc.parsers import get_parser_for_file, BaseParser

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """
    Advanced document analyzer with configurable parsing options.
    """
    
    def __init__(self, config=None, profile=None):
        """
        Initialize the document analyzer.
        
        Args:
            config (dict, optional): Custom configuration settings
            profile (str, optional): Predefined parsing profile
        """
        # Get default profile if none specified
        if profile:
            profile_config = get_parsing_profile(profile)
            self.parsing_config = profile_config["parsing_config"]
            self.output_config = profile_config["output_config"]
        else:
            profile_config = get_parsing_profile("default")
            self.parsing_config = profile_config["parsing_config"]
            self.output_config = profile_config["output_config"]
        
        # Override with custom config if provided
        if config:
            self._apply_custom_config(config)
        
        self.transformer = LLMTransformer()
        self.current_document = None
        self.document_stats = {}
        self.processing_time = {}
    
    def _apply_custom_config(self, config):
        """
        Apply custom configuration settings.
        
        Args:
            config (dict): Custom configuration settings
        """
        parsing_keys = set(vars(self.parsing_config).keys())
        
        for key, value in config.items():
            if key in parsing_keys:
                setattr(self.parsing_config, key, value)
            else:
                setattr(self.output_config, key, value)
    
    def analyze_file(self, file_path, doc_type=None):
        """
        Analyze a document file with optimized parsing based on configuration.
        
        Args:
            file_path (str): Path to the document file
            doc_type (str, optional): Document type to explicitly specify format
            
        Returns:
            Document: Parsed document with analysis results
        """
        start_time = time.time()
        
        try:
            # Validate file
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            file_size = file_path.stat().st_size
            logger.info(f"Analyzing file: {file_path} (Size: {file_size/1024:.2f} KB)")
            
            # Check for large files and handle accordingly
            if (self.parsing_config.max_content_size and 
                file_size > self.parsing_config.max_content_size):
                logger.warning(
                    f"File size ({file_size/1024:.2f} KB) exceeds maximum content size "
                    f"({self.parsing_config.max_content_size/1024:.2f} KB). "
                    "Some content may be truncated."
                )
            
            # Get appropriate parser
            parser = get_parser_for_file(str(file_path), doc_type)
            
            # Apply configuration to parser
            self._configure_parser(parser)
            
            # Parse the document
            raw_parsed_data = parser.parse(str(file_path))
            
            # Extract metadata and elements
            document = Document(
                metadata=raw_parsed_data.get('metadata', {}),
                elements=raw_parsed_data.get('elements', [])
            )
            
            # Apply additional processing based on configuration
            document = self._post_process_document(document)
            
            # Calculate and store document statistics
            self._calculate_document_stats(document)
            
            self.current_document = document
            self.processing_time['parse'] = time.time() - start_time
            
            return document
            
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            self.processing_time['parse'] = time.time() - start_time
            raise
    
    def _configure_parser(self, parser: BaseParser):
        """
        Configure the parser based on parsing configuration.
        
        Args:
            parser: Document parser instance
        """
        # Add configuration parameters to the parser if it supports them
        if hasattr(parser, 'configure'):
            config_dict = {
                'extract_images': self.parsing_config.extract_images,
                'extract_tables': self.parsing_config.extract_tables,
                'extract_diagrams': self.parsing_config.extract_diagrams,
                'extract_code': self.parsing_config.extract_code,
                'use_ocr': self.parsing_config.use_ocr,
                'ocr_languages': self.parsing_config.ocr_languages,
                'ocr_dpi': self.parsing_config.ocr_dpi,
                'preserve_formatting': self.parsing_config.preserve_formatting,
                'table_detection_confidence': self.parsing_config.table_detection_confidence,
                'timeout': self.parsing_config.timeout,
            }
            parser.configure(**config_dict)
    
    def _post_process_document(self, document: Document) -> Document:
        """
        Apply additional processing to the document based on configuration.
        
        Args:
            document: Parsed document
            
        Returns:
            Document: Processed document
        """
        start_time = time.time()
        
        # Add additional metadata
        if 'extraction_level' not in document.metadata:
            document.metadata['extraction_level'] = self.parsing_config.extraction_level
        
        if 'parse_timestamp' not in document.metadata:
            document.metadata['parse_timestamp'] = time.time()
        
        # Apply advanced element classification if using full extraction
        if self.parsing_config.extraction_level == 'full':
            from neuradoc.classifiers.element_classifier import reclassify_elements
            document.elements = reclassify_elements(document.elements)
        
        # Apply parallel processing for large documents if enabled
        if (self.parsing_config.parallel_processing and 
            len(document.elements) > 50):  # Only use for larger documents
            document = self._parallel_process_elements(document)
        
        self.processing_time['post_process'] = time.time() - start_time
        return document
    
    def _parallel_process_elements(self, document: Document) -> Document:
        """
        Process document elements in parallel for improved performance.
        
        Args:
            document: Document to process
            
        Returns:
            Document: Processed document
        """
        # Define a function to process each element
        def process_element(element):
            # Apply additional processing based on element type
            if element.element_type == ElementType.IMAGE and self.parsing_config.use_ocr:
                try:
                    from neuradoc.utils.ocr import extract_text_from_image
                    ocr_text = extract_text_from_image(
                        element.content, 
                        languages=self.parsing_config.ocr_languages
                    )
                    if ocr_text:
                        element.metadata['ocr_text'] = ocr_text
                except Exception as e:
                    logger.warning(f"OCR processing failed: {e}")
            
            return element
        
        # Process elements in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            processed_elements = list(
                executor.map(process_element, document.elements)
            )
        
        document.elements = processed_elements
        return document
    
    def _calculate_document_stats(self, document: Document):
        """
        Calculate and store document statistics.
        
        Args:
            document: Processed document
        """
        stats = {
            'total_elements': len(document.elements),
            'element_types': {},
            'content_size': 0,
            'metadata_fields': len(document.metadata)
        }
        
        # Count element types
        for element in document.elements:
            element_type = element.element_type.name if hasattr(element.element_type, 'name') else str(element.element_type)
            stats['element_types'][element_type] = stats['element_types'].get(element_type, 0) + 1
            
            # Estimate content size
            if element.content:
                try:
                    if hasattr(element.content, '__len__'):
                        stats['content_size'] += len(str(element.content))
                except:
                    pass
        
        self.document_stats = stats
    
    def transform_document(self, document=None, output_config=None):
        """
        Transform a document according to output configuration.
        
        Args:
            document (Document, optional): Document to transform, uses current_document if None
            output_config (OutputConfig, optional): Custom output configuration
            
        Returns:
            Union[str, dict]: Transformed document content
        """
        start_time = time.time()
        
        if document is None:
            document = self.current_document
        
        if document is None:
            raise ValueError("No document to transform. Call analyze_file first.")
        
        config = output_config or self.output_config
        
        try:
            # Apply basic transformation
            result = self.transformer.transform_document(
                document, 
                output_format=config.output_format,
                include_metadata=config.include_metadata
            )
            
            # Apply additional transformations if needed
            if config.apply_transformations:
                result = self._apply_advanced_transformations(result, config)
            
            self.processing_time['transform'] = time.time() - start_time
            return result
            
        except Exception as e:
            logger.error(f"Error transforming document: {e}")
            self.processing_time['transform'] = time.time() - start_time
            raise
    
    def _apply_advanced_transformations(self, content, config):
        """
        Apply advanced transformations to document content.
        
        Args:
            content: Transformed content
            config: Output configuration
            
        Returns:
            Transformed content with advanced processing
        """
        # Add summarization if requested and available
        if config.summarize:
            try:
                if TRANSFORMERS_AVAILABLE:
                    # This would be implemented with transformers or another summarization service
                    logger.info("Summarization requested but not yet implemented")
                else:
                    logger.warning("Summarization requested but transformers library not available")
            except NameError:
                logger.warning("Summarization requested but transformers library not available")
        
        # Add translation if requested and available
        if config.translate and config.target_language:
            try:
                if TRANSFORMERS_AVAILABLE:
                    # This would be implemented with transformers or another translation service
                    logger.info(f"Translation to {config.target_language} requested but not yet implemented")
                else:
                    logger.warning("Translation requested but transformers library not available")
            except NameError:
                logger.warning("Translation requested but transformers library not available")
        
        return content
    
    def extract_specific_content(self, document=None, content_type="text"):
        """
        Extract specific content from a document.
        
        Args:
            document (Document, optional): Document to extract from, uses current_document if None
            content_type (str): Type of content to extract ('text', 'tables', 'images', 'code')
            
        Returns:
            list: Extracted content elements
        """
        if document is None:
            document = self.current_document
        
        if document is None:
            raise ValueError("No document to extract from. Call analyze_file first.")
        
        if content_type == "text":
            text_elements = document.get_elements_by_type(ElementType.TEXT)
            text_elements.extend(document.get_elements_by_type(ElementType.HEADING))
            return text_elements
        
        elif content_type == "tables":
            return document.get_elements_by_type(ElementType.TABLE)
        
        elif content_type == "images":
            return document.get_elements_by_type(ElementType.IMAGE)
        
        elif content_type == "code":
            return document.get_elements_by_type(ElementType.CODE)
        
        else:
            raise ValueError(f"Unknown content type: {content_type}")
    
    def get_processing_summary(self):
        """
        Get a summary of document processing results.
        
        Returns:
            dict: Processing summary
        """
        if not self.current_document:
            return {"status": "No document processed"}
        
        summary = {
            "document": {
                "title": self.current_document.metadata.get('title', 'Untitled'),
                "type": self.current_document.metadata.get('file_type', 'Unknown'),
                "size": self.current_document.metadata.get('size', 0),
            },
            "stats": self.document_stats,
            "timing": {
                "parse_time": self.processing_time.get('parse', 0),
                "post_process_time": self.processing_time.get('post_process', 0),
                "transform_time": self.processing_time.get('transform', 0),
                "total_time": sum(self.processing_time.values()),
            },
            "config": {
                "extraction_level": self.parsing_config.extraction_level,
                "output_format": self.output_config.output_format,
            }
        }
        
        return summary
    
    def batch_process_files(self, file_paths, output_dir=None, doc_types=None):
        """
        Process multiple files in batch mode.
        
        Args:
            file_paths (list): List of file paths to process
            output_dir (str, optional): Directory to save transformed output
            doc_types (list, optional): Document types for each file
            
        Returns:
            list: List of processing results
        """
        results = []
        doc_types = doc_types or [None] * len(file_paths)
        
        for i, file_path in enumerate(file_paths):
            try:
                logger.info(f"Processing file {i+1}/{len(file_paths)}: {file_path}")
                
                # Parse the document
                doc = self.analyze_file(file_path, doc_types[i])
                
                # Transform the document
                transformed = self.transform_document(doc)
                
                # Save to file if output directory provided
                if output_dir:
                    output_path = self._get_output_path(file_path, output_dir)
                    self._save_transformed_content(transformed, output_path)
                
                # Collect results
                results.append({
                    "file": file_path,
                    "success": True,
                    "summary": self.get_processing_summary(),
                })
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                results.append({
                    "file": file_path,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def _get_output_path(self, input_path, output_dir):
        """
        Generate an output file path based on input path and output format.
        
        Args:
            input_path (str): Original file path
            output_dir (str): Output directory
            
        Returns:
            str: Output file path
        """
        filename = os.path.basename(input_path)
        basename, _ = os.path.splitext(filename)
        
        # Determine extension based on output format
        if self.output_config.output_format == 'text':
            ext = '.txt'
        elif self.output_config.output_format == 'markdown':
            ext = '.md'
        elif self.output_config.output_format == 'json':
            ext = '.json'
        elif self.output_config.output_format == 'html':
            ext = '.html'
        else:
            ext = '.txt'
        
        return os.path.join(output_dir, f"{basename}{ext}")
    
    def _save_transformed_content(self, content, output_path):
        """
        Save transformed content to a file.
        
        Args:
            content: Transformed content
            output_path (str): Output file path
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the content based on type
        if isinstance(content, dict):
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2 if self.output_config.pretty_print else None)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(content))
        
        logger.info(f"Saved transformed content to {output_path}")


def analyze_document(file_path, profile=None, config=None, output_format=None, output_file=None):
    """
    Convenience function to analyze a document file with a single call.
    
    Args:
        file_path (str): Path to the document file
        profile (str, optional): Parsing profile name
        config (dict, optional): Custom configuration settings
        output_format (str, optional): Override output format
        output_file (str, optional): Path to save the output
        
    Returns:
        Union[str, dict]: Transformed document content
    """
    analyzer = DocumentAnalyzer(config=config, profile=profile)
    
    # Override output format if specified
    if output_format:
        analyzer.output_config.output_format = output_format
    
    # Analyze the document
    document = analyzer.analyze_file(file_path)
    
    # Transform the document
    result = analyzer.transform_document(document)
    
    # Save to file if specified
    if output_file:
        analyzer._save_transformed_content(result, output_file)
    
    # Return processing summary and result
    return {
        "summary": analyzer.get_processing_summary(),
        "result": result
    }