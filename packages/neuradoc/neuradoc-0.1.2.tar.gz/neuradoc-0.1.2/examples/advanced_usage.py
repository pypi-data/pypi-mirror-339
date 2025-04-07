"""
Advanced usage examples for the neuradoc package with the new analyzer and config features.
"""

import os
import logging
import time
from pathlib import Path
import sys

# Add the parent directory to the path to import neuradoc when running from examples/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import neuradoc
from neuradoc.analyzer import DocumentAnalyzer
from neuradoc.config import ParsingConfig, OutputConfig
from neuradoc.models.element import ElementType

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def example_analyzer_basic(file_path):
    """Example of using the DocumentAnalyzer with default settings."""
    try:
        logger.info("Using DocumentAnalyzer with default settings...")
        
        # Create analyzer with default settings
        analyzer = DocumentAnalyzer()
        
        # Time the parsing operation
        start_time = time.time()
        document = analyzer.analyze_file(file_path)
        parse_time = time.time() - start_time
        
        logger.info(f"Document parsed in {parse_time:.2f} seconds")
        logger.info(f"Document metadata: {document.metadata}")
        logger.info(f"Number of elements: {len(document.elements)}")
        
        # Transform the document to text
        start_time = time.time()
        result = analyzer.transform_document(document)
        transform_time = time.time() - start_time
        
        logger.info(f"Document transformed in {transform_time:.2f} seconds")
        logger.info(f"Transformed result size: {len(result)} characters")
        logger.info(f"Preview: {result[:100]}...")
        
        # Get processing summary
        summary = analyzer.get_processing_summary()
        logger.info(f"Processing summary: {summary}")
        
        return document, result, summary
    
    except Exception as e:
        logger.error(f"Error in basic analyzer example: {e}")
        return None, None, None


def example_analyzer_with_profiles(file_path):
    """Example of using the DocumentAnalyzer with different parsing profiles."""
    results = {}
    
    try:
        logger.info("Testing different parsing profiles...")
        
        # Available profiles: 'default', 'fast', 'detailed', 'llm_ready', 'data_extraction'
        profiles = ['fast', 'default', 'detailed']
        
        for profile in profiles:
            logger.info(f"Using profile: {profile}")
            
            # Create analyzer with the profile
            analyzer = DocumentAnalyzer(profile=profile)
            
            # Time the parsing operation
            start_time = time.time()
            document = analyzer.analyze_file(file_path)
            parse_time = time.time() - start_time
            
            # Transform according to profile's output format
            result = analyzer.transform_document(document)
            
            # Get processing summary
            summary = analyzer.get_processing_summary()
            
            # Store results
            results[profile] = {
                'parse_time': parse_time,
                'element_count': len(document.elements),
                'output_format': analyzer.output_config.output_format,
                'result_size': len(str(result)),
                'summary': summary
            }
            
            logger.info(f"Profile {profile}: {len(document.elements)} elements, " 
                       f"parsed in {parse_time:.2f} seconds, " 
                       f"output format: {analyzer.output_config.output_format}")
        
        # Compare results
        logger.info("\nProfile comparison:")
        for profile, data in results.items():
            logger.info(f"  {profile}:")
            logger.info(f"    Parse time: {data['parse_time']:.2f} seconds")
            logger.info(f"    Elements: {data['element_count']}")
            logger.info(f"    Output format: {data['output_format']}")
            logger.info(f"    Result size: {data['result_size']} characters")
        
        return results
    
    except Exception as e:
        logger.error(f"Error in profile comparison example: {e}")
        return None


def example_custom_configuration(file_path):
    """Example of using custom configuration settings with the DocumentAnalyzer."""
    try:
        logger.info("Using custom configuration settings...")
        
        # Create a custom parsing configuration
        custom_config = {
            'extraction_level': 'standard',
            'extract_images': True,
            'extract_tables': True,
            'extract_diagrams': False,  # Disable diagram extraction
            'use_ocr': False,  # Disable OCR to speed up processing
            'preserve_formatting': True,
            'output_format': 'markdown',  # Use markdown as output format
            'include_metadata': True
        }
        
        # Create analyzer with custom configuration
        analyzer = DocumentAnalyzer(config=custom_config)
        
        # Parse the document
        start_time = time.time()
        document = analyzer.analyze_file(file_path)
        parse_time = time.time() - start_time
        
        logger.info(f"Document parsed with custom config in {parse_time:.2f} seconds")
        logger.info(f"Number of elements: {len(document.elements)}")
        
        # Count element types
        element_counts = {}
        for element in document.elements:
            element_type = element.element_type.name if hasattr(element.element_type, 'name') else str(element.element_type)
            element_counts[element_type] = element_counts.get(element_type, 0) + 1
        
        logger.info(f"Element counts by type: {element_counts}")
        
        # Transform the document
        result = analyzer.transform_document(document)
        
        # Save result to file
        output_dir = Path("./outputs")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "custom_output.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        logger.info(f"Saved custom transformed output to {output_path}")
        
        return document, result
    
    except Exception as e:
        logger.error(f"Error in custom configuration example: {e}")
        return None, None


def example_batch_processing(file_paths):
    """Example of batch processing multiple files."""
    try:
        if not file_paths:
            logger.warning("No files provided for batch processing")
            return None
        
        logger.info(f"Batch processing {len(file_paths)} files...")
        
        # Create output directory
        output_dir = Path("./outputs/batch")
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Process files using convenience function
        start_time = time.time()
        results = neuradoc.batch_process(file_paths, output_dir=str(output_dir), profile="fast")
        total_time = time.time() - start_time
        
        logger.info(f"Batch processing completed in {total_time:.2f} seconds")
        
        # Report results
        success_count = sum(1 for r in results if r.get('success', False))
        logger.info(f"Successfully processed {success_count}/{len(file_paths)} files")
        
        for i, result in enumerate(results):
            if result.get('success', False):
                logger.info(f"File {i+1}: {result['file']} - Success")
            else:
                logger.info(f"File {i+1}: {result['file']} - Failed: {result.get('error', 'Unknown error')}")
        
        return results
    
    except Exception as e:
        logger.error(f"Error in batch processing example: {e}")
        return None


def example_available_profiles():
    """Example of retrieving and displaying available parsing profiles."""
    try:
        logger.info("Getting available parsing profiles...")
        
        profiles = neuradoc.get_available_profiles()
        
        logger.info(f"Found {len(profiles)} available profiles:")
        for name, profile in profiles.items():
            logger.info(f"  {name}:")
            logger.info(f"    Description: {profile['description']}")
            logger.info(f"    Extraction Level: {profile['extraction_level']}")
            logger.info(f"    Output Format: {profile['output_format']}")
        
        return profiles
    
    except Exception as e:
        logger.error(f"Error getting available profiles: {e}")
        return None


def example_direct_analysis(file_path):
    """Example of using the direct analyze_document function."""
    try:
        logger.info("Using the direct analyze_document function...")
        
        # Analyze the document with the convenience function
        start_time = time.time()
        result = neuradoc.analyze_document(
            file_path, 
            profile="llm_ready",
            output_format="markdown",
            output_file="./outputs/direct_output.md"
        )
        total_time = time.time() - start_time
        
        logger.info(f"Document analyzed in {total_time:.2f} seconds")
        
        # Print summary
        summary = result["summary"]
        logger.info(f"Document: {summary['document']['title']}")
        logger.info(f"Element count: {summary['stats']['total_elements']}")
        logger.info(f"Processing times: {summary['timing']}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error in direct analysis example: {e}")
        return None


def run_examples():
    """Run all advanced examples."""
    if len(sys.argv) < 2:
        logger.error("Please provide at least one file path as an argument.")
        logger.info("Usage: python advanced_usage.py <file_path> [<additional_file_path> ...]")
        return
    
    file_path = sys.argv[1]
    additional_files = sys.argv[2:] if len(sys.argv) > 2 else []
    all_files = [file_path] + additional_files
    
    if not os.path.exists(file_path):
        logger.error(f"Primary file not found: {file_path}")
        return
    
    # Run examples
    logger.info("NEURADOC ADVANCED USAGE EXAMPLES")
    logger.info("===============================")
    
    # Display available profiles
    example_available_profiles()
    
    # Basic analyzer usage
    example_analyzer_basic(file_path)
    
    # Profile comparison
    example_analyzer_with_profiles(file_path)
    
    # Custom configuration
    example_custom_configuration(file_path)
    
    # Direct analysis
    example_direct_analysis(file_path)
    
    # Batch processing (if additional files provided)
    if additional_files:
        valid_files = [f for f in all_files if os.path.exists(f)]
        example_batch_processing(valid_files)
    else:
        logger.info("Skipping batch processing example (requires additional files)")
    
    logger.info("All examples completed!")


if __name__ == "__main__":
    run_examples()