"""
Basic usage examples for the neuradoc package.
"""

import os
import logging
from pathlib import Path
import sys

# Add the parent directory to the path to import neuradoc when running from examples/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from neuradoc import load_document
from neuradoc.models.element import ElementType
from neuradoc.transformers.llm_transformer import LLMTransformer, transform_to_context_chunks
from neuradoc.utils.ocr import extract_text_from_image
from neuradoc.extractors.table_extractor import table_to_markdown, table_to_dataframe

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def example_load_document(file_path):
    """Example of loading and parsing a document."""
    try:
        logger.info(f"Loading document: {file_path}")
        doc = load_document(file_path)
        
        logger.info(f"Document loaded successfully: {doc}")
        logger.info(f"Document metadata: {doc.metadata}")
        logger.info(f"Number of elements: {len(doc.elements)}")
        
        # Count elements by type
        element_counts = {}
        for element in doc.elements:
            element_type = element.element_type.name if hasattr(element.element_type, 'name') else str(element.element_type)
            element_counts[element_type] = element_counts.get(element_type, 0) + 1
        
        logger.info(f"Element counts by type: {element_counts}")
        
        return doc
    
    except Exception as e:
        logger.error(f"Error loading document: {e}")
        return None


def example_extract_text(doc):
    """Example of extracting text from a document."""
    if not doc:
        return
    
    try:
        logger.info("Extracting text content...")
        text_content = doc.get_text_content()
        
        logger.info(f"Extracted {len(text_content)} characters of text")
        
        # Print a preview of the text
        preview_length = min(200, len(text_content))
        logger.info(f"Text preview: {text_content[:preview_length]}...")
        
        # Get text elements specifically
        text_elements = doc.get_elements_by_type(ElementType.TEXT)
        logger.info(f"Found {len(text_elements)} text elements")
        
        return text_content
    
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return None


def example_extract_tables(doc):
    """Example of extracting tables from a document."""
    if not doc:
        return
    
    try:
        logger.info("Extracting tables...")
        tables = doc.get_tables()
        
        logger.info(f"Extracted {len(tables)} tables")
        
        for i, table in enumerate(tables[:3]):  # Show only first 3 tables
            logger.info(f"Table {i+1}:")
            
            # Convert to markdown for display
            md_table = table_to_markdown(table)
            logger.info(md_table)
            
            # Convert to DataFrame
            df = table_to_dataframe(table)
            if not df.empty:
                logger.info(f"DataFrame shape: {df.shape}")
        
        return tables
    
    except Exception as e:
        logger.error(f"Error extracting tables: {e}")
        return None


def example_extract_images(doc):
    """Example of extracting images from a document."""
    if not doc:
        return
    
    try:
        logger.info("Extracting images...")
        image_elements = doc.get_elements_by_type(ElementType.IMAGE)
        
        logger.info(f"Extracted {len(image_elements)} images")
        
        # Process some images
        for i, element in enumerate(image_elements[:3]):  # Show only first 3 images
            image = element.content
            if hasattr(image, 'size'):
                logger.info(f"Image {i+1}: Size {image.size}, Mode {image.mode}")
                
                # Example of OCR if it's available
                try:
                    text = extract_text_from_image(image)
                    if text and text.strip():
                        logger.info(f"OCR Text from image {i+1}: {text[:100]}...")
                except Exception as e:
                    logger.info(f"OCR not available or failed: {e}")
            else:
                logger.info(f"Image {i+1}: {str(image)[:100]}...")
        
        return image_elements
    
    except Exception as e:
        logger.error(f"Error extracting images: {e}")
        return None


def example_llm_transform(doc):
    """Example of transforming a document to LLM-ready formats."""
    if not doc:
        return
    
    try:
        logger.info("Transforming document to LLM-ready formats...")
        transformer = LLMTransformer()
        
        # Transform to different formats
        text_format = transformer.transform_document(doc, output_format='text')
        logger.info(f"Text format length: {len(text_format)} characters")
        
        markdown_format = transformer.transform_document(doc, output_format='markdown')
        logger.info(f"Markdown format length: {len(markdown_format)} characters")
        
        json_format = transformer.transform_document(doc, output_format='json')
        logger.info(f"JSON format: {len(str(json_format))} characters")
        
        # Create context chunks
        logger.info("Creating context chunks...")
        chunks = transform_to_context_chunks(doc, chunk_size=1000, overlap=100, format='text')
        logger.info(f"Created {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks[:2]):  # Show only first 2 chunks
            logger.info(f"Chunk {i+1} length: {len(chunk)} characters")
            logger.info(f"Chunk {i+1} preview: {chunk[:100]}...")
        
        # Save document to file
        output_dir = Path("./outputs")
        output_dir.mkdir(exist_ok=True)
        
        doc.save(output_dir / "output.json", format="json")
        logger.info(f"Saved document as JSON to {output_dir / 'output.json'}")
        
        doc.save(output_dir / "output.md", format="markdown")
        logger.info(f"Saved document as Markdown to {output_dir / 'output.md'}")
        
        return {
            'text': text_format,
            'markdown': markdown_format,
            'json': json_format,
            'chunks': chunks
        }
    
    except Exception as e:
        logger.error(f"Error transforming document: {e}")
        return None


def run_examples():
    """Run all examples if a file path is provided."""
    if len(sys.argv) < 2:
        logger.error("Please provide a file path as an argument.")
        logger.info("Usage: python basic_usage.py <file_path>")
        return
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return
    
    # Run examples
    doc = example_load_document(file_path)
    if doc:
        example_extract_text(doc)
        example_extract_tables(doc)
        example_extract_images(doc)
        example_llm_transform(doc)


if __name__ == "__main__":
    run_examples()
